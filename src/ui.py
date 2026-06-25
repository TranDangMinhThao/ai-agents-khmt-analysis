"""Helper dùng chung cho các trang Streamlit: theme xanh/trắng, hero banner, filter."""
import streamlit as st

from . import data_loader as dl

# Bảng màu chủ đạo (xanh dương + trắng)
BLUE_900 = "#1e3a8a"
BLUE_700 = "#1d4ed8"
BLUE_600 = "#2563eb"
BLUE_500 = "#3b82f6"
BLUE_100 = "#dbeafe"
BLUE_050 = "#eff6ff"

_CSS = f"""
<style>
.stApp {{ background:#ffffff; }}
/* Tiêu đề màu xanh đậm */
h1, h2, h3 {{ color:{BLUE_900}; font-weight:700; }}
/* Sidebar nền xanh nhạt */
section[data-testid="stSidebar"] {{
    background:{BLUE_050};
    border-right:1px solid {BLUE_100};
}}
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{ color:{BLUE_700}; }}
/* Thẻ chỉ số (metric) nổi bật */
div[data-testid="stMetric"] {{
    background:linear-gradient(135deg,{BLUE_050} 0%,#ffffff 100%);
    border:1px solid {BLUE_100};
    border-left:5px solid {BLUE_600};
    border-radius:12px;
    padding:14px 18px;
    box-shadow:0 2px 8px rgba(37,99,235,.10);
}}
div[data-testid="stMetricValue"] {{ color:{BLUE_700}; font-weight:700; }}
div[data-testid="stMetricLabel"] p {{ color:#475569; font-weight:600; }}
/* Hero banner */
.hero {{
    background:linear-gradient(120deg,{BLUE_900} 0%,{BLUE_600} 55%,{BLUE_500} 100%);
    padding:26px 32px; border-radius:16px; color:#fff;
    box-shadow:0 10px 28px rgba(37,99,235,.28); margin-bottom:18px;
}}
.hero h1 {{ color:#ffffff !important; margin:0; font-size:30px; line-height:1.2; }}
.hero p {{ color:#e0ecff; margin:8px 0 0; font-size:15px; }}
.hero .tag {{
    display:inline-block; margin-top:12px; padding:4px 12px; font-size:12px;
    background:rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.35);
    border-radius:20px; color:#fff;
}}
/* Tiêu đề mục có gạch xanh bên trái */
h2 {{ border-left:6px solid {BLUE_600}; padding-left:12px; }}
/* Thanh ngang */
hr {{ border-color:{BLUE_100}; }}
/* Bảng */
div[data-testid="stDataFrame"] {{ border:1px solid {BLUE_100}; border-radius:10px; }}
/* Nút, tab nhấn xanh */
.stTabs [aria-selected="true"] {{ color:{BLUE_700}; }}
</style>
"""


def page_config(title: str = ""):
    """Cấu hình trang + CSS. An toàn khi gọi nhiều lần (router + page) trong 1 lần chạy."""
    if not st.session_state.get("_page_configured"):
        st.set_page_config(page_title="AI Agents trong ngành Khoa học Máy tính",
                           layout="wide")
        st.session_state["_page_configured"] = True
    st.markdown(_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str = "", tag: str = ""):
    tag_html = f'<span class="tag">{tag}</span>' if tag else ""
    st.markdown(
        f'<div class="hero"><h1>{title}</h1>'
        f'<p>{subtitle}</p>{tag_html}</div>',
        unsafe_allow_html=True)


def sidebar_filter():
    """Bộ lọc nghề dùng chung; trả về bảng task đã lọc."""
    df = dl.task_table()
    occs = sorted(df["Occupation"].unique())
    st.sidebar.header("Bộ lọc")
    chosen = st.sidebar.multiselect(
        "Nghề (Khoa học Máy tính)", options=occs, default=occs,
        help="Phạm vi mặc định: nhóm O*NET 15-12xx + Computer & Information Systems Managers.")
    if not chosen:
        chosen = occs
    out = df[df["Occupation"].isin(chosen)]
    st.sidebar.caption(f"Đang xem: {out['Task ID'].nunique()} tác vụ / {len(chosen)} nghề")
    st.sidebar.divider()
    st.sidebar.caption("Nguồn: WORKBank (mong muốn người lao động + năng lực chuyên gia + "
                       "danh mục tác vụ O*NET). Mọi số tái tạo từ CSV gốc.")
    return out
