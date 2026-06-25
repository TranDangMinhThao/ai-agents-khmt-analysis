"""Trang 4 - So sánh theo nghề: nghề nào sẵn sàng cho AI agent nhất."""
import plotly.express as px
import streamlit as st

from src import ui
from src import analysis
from src import config

ui.page_config("So sánh theo nghề")
ui.hero("So sánh theo nghề", "Nghề nào vừa được mong muốn vừa khả thi nhất cho AI agent")

df = ui.sidebar_filter()
occ = analysis.occupation_summary(df)

st.subheader("Bản đồ nghề: Mong muốn x Năng lực AI")
fig = px.scatter(occ, x="nang_luc_AI", y="mong_muon", text="Occupation",
                 size="so_task", color="human_agency",
                 color_continuous_scale=config.HAS_COLOR,
                 labels={"nang_luc_AI": "Năng lực AI TB (1-5)",
                         "mong_muon": "Mong muốn TB (1-5)",
                         "human_agency": "HAS TB"})
fig.add_hline(y=config.THRESHOLD, line_dash="dash", line_color="#888")
fig.add_vline(x=config.THRESHOLD, line_dash="dash", line_color="#888")
fig.update_traces(textposition="top center", textfont_size=9)
fig.update_layout(height=620, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig, use_container_width=True)
st.caption("Góc trên-phải = nghề vừa MUỐN vừa KHẢ THI nhất cho AI agent. "
           "Màu chỉ mức Human Agency mong muốn.")

st.divider()
st.subheader("Chênh lệch Năng lực AI - Mong muốn (theo nghề)")
occ2 = occ.sort_values("chenh_lech")
fig2 = px.bar(occ2, x="chenh_lech", y="Occupation", orientation="h",
              color="chenh_lech", color_continuous_scale="RdBu",
              labels={"chenh_lech": "Năng lực AI - Mong muốn", "Occupation": ""})
fig2.update_layout(height=520, coloraxis_showscale=False,
                   margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig2, use_container_width=True)
st.markdown(
    "- **Dương (xanh)**: AI làm được *nhiều hơn* người lao động mong muốn "
    "→ cần quản trị thay đổi, tránh ép buộc.\n"
    "- **Âm (đỏ)**: người lao động *muốn nhiều hơn* năng lực AI hiện tại "
    "→ cơ hội R&D / xây công cụ mới."
)

with st.expander("Bảng chi tiết theo nghề"):
    show = occ.rename(columns={"Occupation": "Nghề", "so_task": "Số tác vụ",
                               "mong_muon": "Mong muốn", "nang_luc_AI": "Năng lực AI",
                               "human_agency": "HAS", "chenh_lech": "Chênh lệch",
                               "luong_TB": "Lương TB năm ($)"})
    st.dataframe(show, use_container_width=True, hide_index=True)
