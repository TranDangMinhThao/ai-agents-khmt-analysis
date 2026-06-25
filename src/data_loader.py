"""
Lop du lieu: doc 4 CSV, lam sach, join, loc pham vi Khoa hoc May tinh (CS).
Tat ca con so trong dashboard deu sinh ra tu day -> tai tao duoc (RULE 4).

Chay doc lap de kiem tra:  py src/data_loader.py
"""
import ast
import numpy as np
import pandas as pd

from . import config
from .config import DATA, is_cs_code

# Cache cua Streamlit neu co; neu khong (chay bang `py` thuan) thi dung no-op.
try:
    import streamlit as st
    cache = st.cache_data
except Exception:  # streamlit chua cai / chay ngoai app
    def cache(func=None, **_):
        return func if func else (lambda f: f)


REQ_COLS = [
    "Physical Action Requirement",
    "Interpersonal Communication Requirement",
    "Involved Uncertainty",
    "Domain Expertise Requirement",
]
LLM_USAGE_COLS = [
    "LLM Usage by Type - Information Access",
    "LLM Usage by Type - Edit",
    "LLM Usage by Type - Idea Generation",
    "LLM Usage by Type - Communication",
    "LLM Usage by Type - Analysis",
    "LLM Usage by Type - Decision",
    "LLM Usage by Type - Coding",
    "LLM Usage by Type - System Design",
    "LLM Usage by Type - Data Processing",
]
USAGE_FREQ_ORDER = ["Never", "Monthly", "Weekly", "Daily"]


def _num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _first_skill(cell: str) -> str:
    """Skill (O*NET Work Activity) luu dang list-string "['...']" -> lay phan tu dau."""
    try:
        val = ast.literal_eval(cell)
        if isinstance(val, (list, tuple)) and val:
            return str(val[0])
    except Exception:
        pass
    return ""


@cache
def load_raw() -> dict:
    desires = pd.read_csv(DATA["desires"], dtype={"Task ID": str, "User ID": str})
    expert = pd.read_csv(DATA["expert"], dtype={"Task ID": str, "User ID": str})
    tasks = pd.read_csv(DATA["tasks"], dtype={"Task ID": str})
    meta = pd.read_csv(DATA["metadata"], dtype={"User ID": str})

    for col in ["Automation Desire Rating", "Human Agency Scale Rating",
                "Core Skill Rating", "Job Security Rating", "Enjoyment Rating", *REQ_COLS]:
        if col in desires:
            desires[col] = _num(desires[col])
    for col in ["Automation Capacity Rating", "Human Agency Scale Rating", *REQ_COLS]:
        if col in expert:
            expert[col] = _num(expert[col])
    for col in ["Importance", "Relevance", "Frequency",
                "Occupation Mean Annual Wage", "Occupation Employment"]:
        if col in tasks:
            tasks[col] = _num(tasks[col])
    return {"desires": desires, "expert": expert, "tasks": tasks, "meta": meta}


@cache
def cs_occupations() -> pd.DataFrame:
    """Cac nghe thuoc pham vi CS, kem ma SOC (duy nhat / occupation)."""
    tasks = load_raw()["tasks"]
    occ = (tasks[["Occupation (O*NET-SOC Title)", "O*NET-SOC Code"]]
           .dropna().drop_duplicates("Occupation (O*NET-SOC Title)"))
    occ = occ[occ["O*NET-SOC Code"].map(is_cs_code)]
    return occ.rename(columns={"Occupation (O*NET-SOC Title)": "Occupation",
                               "O*NET-SOC Code": "SOC"}).reset_index(drop=True)


@cache
def task_table() -> pd.DataFrame:
    """
    Bang 1-dong-moi-task (pham vi CS): mong muon nguoi lao dong vs nang luc AI,
    da gan zone va metadata nghe (wage, employment, importance...).
    """
    raw = load_raw()
    cs_occ = set(cs_occupations()["Occupation"])

    d = raw["desires"][raw["desires"]["Occupation (O*NET-SOC Title)"].isin(cs_occ)]
    e = raw["expert"][raw["expert"]["Occupation (O*NET-SOC Title)"].isin(cs_occ)]

    dg = d.groupby("Task ID").agg(
        worker_desire=("Automation Desire Rating", "mean"),
        worker_has=("Human Agency Scale Rating", "mean"),
        n_workers=("User ID", "nunique"),
        Occupation=("Occupation (O*NET-SOC Title)", "first"),
        Task=("Task", "first"),
    )
    for c in REQ_COLS:
        dg[c] = d.groupby("Task ID")[c].mean()

    eg = e.groupby("Task ID").agg(
        ai_capability=("Automation Capacity Rating", "mean"),
        expert_has=("Human Agency Scale Rating", "mean"),
        n_experts=("User ID", "nunique"),
    )

    df = dg.join(eg, how="inner").reset_index()  # chi giu task co CA worker & expert

    tinfo = (raw["tasks"].drop_duplicates("Task ID")
             .set_index("Task ID")[["O*NET-SOC Code", "Task Type", "Importance",
                                     "Relevance", "Frequency",
                                     "Occupation Mean Annual Wage",
                                     "Occupation Employment",
                                     "Skill (O*NET Work Activity)"]])
    df = df.join(tinfo, on="Task ID")
    df["Skill"] = df["Skill (O*NET Work Activity)"].map(_first_skill)

    df["zone"] = [config.classify_zone(dd, cc)
                  for dd, cc in zip(df["worker_desire"], df["ai_capability"])]
    df["gap"] = df["ai_capability"] - df["worker_desire"]  # >0: AI vuot mong muon
    return df


@cache
def cs_workers() -> pd.DataFrame:
    """Ho so nguoi lao dong CS (tu metadata)."""
    raw = load_raw()
    cs_occ = set(cs_occupations()["Occupation"])
    m = raw["meta"][raw["meta"]["Occupation (O*NET-SOC Title)"].isin(cs_occ)].copy()
    return m


@cache
def llm_usage_long() -> pd.DataFrame:
    """Bang dai cho 9 loai su dung LLM cua nguoi lao dong CS (de ve heatmap)."""
    m = cs_workers()
    rows = []
    for col in LLM_USAGE_COLS:
        if col not in m:
            continue
        label = col.replace("LLM Usage by Type - ", "")
        vc = m[col].value_counts()
        total = vc.sum()
        for freq in USAGE_FREQ_ORDER:
            rows.append({"Loai": label, "Tan suat": freq,
                         "So nguoi": int(vc.get(freq, 0)),
                         "Ty le": (vc.get(freq, 0) / total * 100) if total else 0})
    return pd.DataFrame(rows)


@cache
def desires_cs() -> pd.DataFrame:
    raw = load_raw()
    cs_occ = set(cs_occupations()["Occupation"])
    return raw["desires"][raw["desires"]["Occupation (O*NET-SOC Title)"].isin(cs_occ)].copy()


if __name__ == "__main__":
    tt = task_table()
    print("CS occupations:", len(cs_occupations()))
    print("Task table rows (task co ca worker+expert):", len(tt))
    print("CS workers (metadata):", len(cs_workers()))
    print("\nZone counts:")
    print(tt["zone"].value_counts())
    print("\nMean worker_desire: %.2f | mean ai_capability: %.2f | mean worker_has: %.2f"
          % (tt["worker_desire"].mean(), tt["ai_capability"].mean(), tt["worker_has"].mean()))
    print("\nPer-occupation task counts:")
    print(tt["Occupation"].value_counts())
