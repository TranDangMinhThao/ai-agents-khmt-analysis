"""Trang 1 - Tổng quan dữ liệu & chất lượng."""
import plotly.express as px
import streamlit as st

from src import ui
from src import data_loader as dl
from src import analysis
from src import config

ui.page_config("Tổng quan")
ui.hero("Tổng quan dữ liệu", "Quy mô, phân bố theo nghề và chất lượng dữ liệu WORKBank (phạm vi KHMT)")

df = ui.sidebar_filter()
k = analysis.kpis(df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Tác vụ phân tích", k["n_tasks"])
c2.metric("Nghề CS", k["n_occ"])
c3.metric("Mong muốn TB (người lao động)", k["mean_desire"])
c4.metric("Năng lực AI TB (chuyên gia)", k["mean_cap"])

st.divider()
st.subheader("Số tác vụ theo nghề")
occ = analysis.occupation_summary(df).sort_values("so_task", ascending=True)
fig = px.bar(occ, x="so_task", y="Occupation", orientation="h",
             labels={"so_task": "Số tác vụ", "Occupation": ""},
             color="so_task", color_continuous_scale="Blues")
fig.update_layout(height=520, coloraxis_showscale=False, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig, width='stretch')

st.subheader("Mong muốn người lao động vs Năng lực AI (trung bình mỗi nghề)")
melt = occ.melt(id_vars="Occupation", value_vars=["mong_muon", "nang_luc_AI"],
                var_name="Chỉ số", value_name="Điểm (1-5)")
melt["Chỉ số"] = melt["Chỉ số"].map({"mong_muon": "Mong muốn (người lao động)",
                                     "nang_luc_AI": "Năng lực AI (chuyên gia)"})
fig2 = px.bar(melt, x="Điểm (1-5)", y="Occupation", color="Chỉ số", barmode="group",
              orientation="h", color_discrete_sequence=[config.COLOR_WORKER, config.COLOR_EXPERT])
fig2.update_layout(height=560, margin=dict(l=10, r=10, t=10, b=10),
                   legend=dict(orientation="h", y=1.05))
st.plotly_chart(fig2, width='stretch')

st.divider()
st.subheader("Chất lượng dữ liệu (minh bạch - không giấu thiếu sót)")
raw = dl.load_raw()
st.markdown(
    f"""
- 4 bảng liên kết qua **Task ID** / **User ID**. Bảng này chỉ giữ tác vụ có **CẢ**
  mong muốn người lao động **và** đánh giá chuyên gia → còn **{k['n_tasks']} tác vụ** CS.
- Toàn bộ `desires` có {len(raw['desires']):,} dòng; `expert` {len(raw['expert']):,} dòng;
  `tasks` (danh mục) {len(raw['tasks']):,} dòng; `metadata` {len(raw['meta']):,} người.
- Cột `Zip Code` trong metadata thiếu nhiều (để trống) → KHÔNG dùng để suy luận địa lý.
- Mỗi rating là số nguyên 1-5; giá trị rỗng đã bị loại khi tính trung bình.
    """
)
with st.expander("Xem bảng dữ liệu theo nghề"):
    show = occ.sort_values("so_task", ascending=False).rename(columns={
        "Occupation": "Nghề", "so_task": "Số tác vụ", "mong_muon": "Mong muốn",
        "nang_luc_AI": "Năng lực AI", "human_agency": "HAS", "chenh_lech": "Chênh lệch",
        "luong_TB": "Lương TB năm ($)"})
    st.dataframe(show, use_container_width=True, hide_index=True)
