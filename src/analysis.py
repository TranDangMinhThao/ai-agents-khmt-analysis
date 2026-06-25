"""
Tang phan tich: bien bang du lieu thanh chi so / xep hang / khuyen nghi.
Khong ve gi o day (tach bach data - view). Moi ket luan deu tu so that.
"""
import pandas as pd

from . import config


def zone_summary(df: pd.DataFrame) -> pd.DataFrame:
    s = (df.groupby("zone").size().reindex(config.ZONE_ORDER, fill_value=0)
         .rename("So task").reset_index())
    s["Ty le %"] = (s["So task"] / s["So task"].sum() * 100).round(1)
    s["Mo ta"] = s["zone"].map(config.ZONE_DESC)
    return s


def occupation_summary(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("Occupation").agg(
        so_task=("Task ID", "nunique"),
        mong_muon=("worker_desire", "mean"),
        nang_luc_AI=("ai_capability", "mean"),
        human_agency=("worker_has", "mean"),
        luong_TB=("Occupation Mean Annual Wage", "first"),
    ).reset_index()
    g["chenh_lech"] = (g["nang_luc_AI"] - g["mong_muon"]).round(2)
    for c in ["mong_muon", "nang_luc_AI", "human_agency"]:
        g[c] = g[c].round(2)
    return g.sort_values("mong_muon", ascending=False)


def top_tasks(df: pd.DataFrame, zone: str, n: int = 10) -> pd.DataFrame:
    sub = df[df["zone"] == zone].copy()
    if zone == config.ZONE_GREEN:
        sub = sub.sort_values(["worker_desire", "ai_capability"], ascending=False)
    elif zone == config.ZONE_RND:
        sub = sub.sort_values(["worker_desire", "ai_capability"], ascending=[False, True])
    elif zone == config.ZONE_RED:
        sub = sub.sort_values(["ai_capability", "worker_desire"], ascending=[False, True])
    else:
        sub = sub.sort_values(["worker_desire", "ai_capability"], ascending=True)
    cols = ["Task", "Occupation", "worker_desire", "ai_capability",
            "worker_has", "n_workers"]
    return sub[cols].head(n).reset_index(drop=True)


def has_distribution(desires_cs: pd.DataFrame) -> pd.DataFrame:
    vc = desires_cs["Human Agency Scale Rating"].dropna().astype(int).value_counts()
    total = vc.sum()
    rows = []
    for h in range(config.RATING_MIN, config.RATING_MAX + 1):
        rows.append({"HAS": h, "Nhan": config.HAS_LABEL[h],
                     "So luot": int(vc.get(h, 0)),
                     "Ty le %": round(vc.get(h, 0) / total * 100, 1) if total else 0})
    return pd.DataFrame(rows)


def kpis(df: pd.DataFrame) -> dict:
    return {
        "n_tasks": int(df["Task ID"].nunique()),
        "n_occ": int(df["Occupation"].nunique()),
        "mean_desire": round(df["worker_desire"].mean(), 2),
        "mean_cap": round(df["ai_capability"].mean(), 2),
        "mean_has": round(df["worker_has"].mean(), 2),
        "pct_green": round((df["zone"] == config.ZONE_GREEN).mean() * 100, 1),
        "pct_red": round((df["zone"] == config.ZONE_RED).mean() * 100, 1),
    }
