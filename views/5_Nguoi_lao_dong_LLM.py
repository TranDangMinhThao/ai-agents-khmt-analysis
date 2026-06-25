"""Trang 5 - Người lao động CS & hiện trạng dùng LLM trong công việc."""
import plotly.express as px
import streamlit as st

from src import ui
from src import data_loader as dl
from src.data_loader import USAGE_FREQ_ORDER

ui.page_config("Người lao động & LLM")
ui.hero("Người lao động CS & hiện trạng dùng LLM",
        "Mức độ và cách người lao động ngành KHMT đang sử dụng LLM trong công việc")
ui.sidebar_filter()  # giữ bộ lọc đồng nhất ở sidebar (trang này xét toàn bộ worker CS)

workers = dl.cs_workers()
st.caption(f"Dữ liệu từ {len(workers)} người lao động CS trong `domain_worker_metadata.csv`. "
           "Trang này xét toàn bộ người lao động CS (không phụ thuộc bộ lọc tác vụ).")

# --- LLM Use in Work + Familiarity ---
c1, c2 = st.columns(2)
with c1:
    st.subheader("Đã dùng LLM trong công việc?")
    vc = workers["LLM Use in Work"].value_counts().reset_index()
    vc.columns = ["Trả lời", "Số người"]
    fig = px.pie(vc, names="Trả lời", values="Số người", hole=0.45,
                 color_discrete_sequence=px.colors.sequential.Blues_r)
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=10, b=10),
                      legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig, width='stretch')
with c2:
    st.subheader("Mức độ quen thuộc LLM")
    vc2 = workers["LLM Familiarity"].value_counts().reset_index()
    vc2.columns = ["Mức độ", "Số người"]
    fig2 = px.bar(vc2, x="Số người", y="Mức độ", orientation="h", color="Số người",
                  color_continuous_scale="Blues")
    fig2.update_layout(height=380, coloraxis_showscale=False,
                       margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig2, width='stretch')

st.divider()
st.subheader("Tần suất dùng LLM theo 9 loại công việc (heatmap)")
long = dl.llm_usage_long()
pivot = long.pivot(index="Loai", columns="Tan suat", values="Ty le")[USAGE_FREQ_ORDER]
fig3 = px.imshow(pivot, text_auto= True, aspect="auto", color_continuous_scale="Blues",
                 labels=dict(color="% người"))
fig3.update_layout(height=460, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig3, use_container_width=True)
st.caption("Mỗi ô = % người lao động CS dùng LLM cho loại đó ở tần suất tương ứng. "
           "Hàng sáng bên phải (Weekly/Daily) = loại công việc LLM đã thâm nhập sâu.")

st.divider()
st.subheader("Thái độ về AI")
attitudes = ["AI Tedious Work Attitude", "AI Job Importance Attitude",
             "AI Daily Interest Attitude", "AI Suffering Attitude"]
labels = {"AI Tedious Work Attitude": "AI giúp việc nhàm chán",
          "AI Job Importance Attitude": "AI ảnh hưởng tầm quan trọng công việc",
          "AI Daily Interest Attitude": "Quan tâm AI hằng ngày",
          "AI Suffering Attitude": "Lo ngại AI gây tổn hại"}
sel = st.selectbox("Chọn thái độ", attitudes, format_func=lambda x: labels[x])
vc3 = workers[sel].value_counts().reset_index()
vc3.columns = ["Mức độ đồng ý", "Số người"]
fig4 = px.bar(vc3, x="Mức độ đồng ý", y="Số người", color="Số người",
              color_continuous_scale="Blues")
fig4.update_layout(height=380, coloraxis_showscale=False, xaxis_tickangle=-15,
                   margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig4, use_container_width=True)
