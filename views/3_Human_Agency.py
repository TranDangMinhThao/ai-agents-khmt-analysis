"""Trang 3 - Human Agency Scale: người làm CS muốn AI tự chủ tới đâu."""
import plotly.express as px
import streamlit as st

from src import ui
from src import data_loader as dl
from src import analysis
from src import config

ui.page_config("Human Agency")
ui.hero("Human Agency Scale (HAS)",
        "Thang H1 (AI làm toàn bộ) → H5 (con người làm toàn bộ): người lao động muốn giữ vai trò tới đâu khi có AI")

df = ui.sidebar_filter()
des = dl.desires_cs()
des = des[des["Occupation (O*NET-SOC Title)"].isin(df["Occupation"].unique())]

dist = analysis.has_distribution(des)

c1, c2 = st.columns([2, 1])
with c1:
    fig = px.bar(dist, x="Nhan", y="So luot", color="HAS",
                 color_continuous_scale=config.HAS_COLOR,
                 labels={"Nhan": "", "So luot": "Số lượt chấm"})
    fig.update_layout(height=460, coloraxis_showscale=False, xaxis_tickangle=-15,
                      margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)
with c2:
    mean_has = des["Human Agency Scale Rating"].mean()
    st.metric("HAS trung bình", f"{mean_has:.2f}")
    if mean_has < 3:
        st.success("HAS < 3: người lao động CS NGHIÊNG về giao nhiều hơn cho AI "
                   "(AI làm chính, người giám sát).")
    else:
        st.warning("HAS >= 3: người lao động CS muốn GIỮ vai trò chủ đạo, AI chỉ hỗ trợ.")
    distv = dist.rename(columns={"Nhan": "Mức HAS", "So luot": "Số lượt", "Ty le %": "Tỷ lệ %"})
    st.dataframe(distv[["Mức HAS", "Số lượt", "Tỷ lệ %"]], hide_index=True, use_container_width=True)

st.divider()
st.subheader("HAS trung bình theo nghề")
occ = (df.groupby("Occupation")["worker_has"].mean()
       .round(2).sort_values().reset_index())
fig2 = px.bar(occ, x="worker_has", y="Occupation", orientation="h",
              color="worker_has", color_continuous_scale=config.HAS_COLOR,
              labels={"worker_has": "HAS trung bình (1-5)", "Occupation": ""})
fig2.add_vline(x=config.THRESHOLD, line_dash="dash", line_color="#888")
fig2.update_layout(height=520, coloraxis_showscale=False,
                   margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig2, use_container_width=True)
st.caption("Nghề bên trái vạch đứt (HAS<3): có thể giao AI tự chủ nhiều hơn. "
           "Bên phải: nên thiết kế AI agent dạng 'human-in-the-loop' (người trong vòng lặp).")
