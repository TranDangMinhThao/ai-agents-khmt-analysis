"""Trang chủ - giới thiệu đề tài & điều hướng."""
import streamlit as st

from src import ui
from src import data_loader as dl
from src import analysis

ui.page_config("Trang chủ")
ui.hero("Ứng dụng AI Agents trong ngành Khoa học Máy tính",
        "Phân tích hiện trạng & khuyến nghị triển khai AI agents - dữ liệu WORKBank",
        tag="Môn: Trực quan hóa dữ liệu")

df = dl.task_table()
k = analysis.kpis(df)
workers = dl.cs_workers()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Nghề CS", k["n_occ"])
c2.metric("Tác vụ phân tích", k["n_tasks"],
          help="Tác vụ có CẢ mong muốn người lao động và đánh giá chuyên gia")
c3.metric("Người lao động CS", len(workers))
c4.metric("Mong muốn TB / Năng lực AI TB", f'{k["mean_desire"]} / {k["mean_cap"]}')

st.divider()

st.subheader("Đề tài & cách tiếp cận")
st.markdown(
    """
**Câu hỏi:** Trong ngành Khoa học Máy tính (KHMT), *AI agents nên được ứng dụng vào
đâu* - dựa trên cả **mong muốn của người lao động** lẫn **năng lực thực tế của AI**?

Bộ dữ liệu **WORKBank** cho phép trả lời từ hai phía một cách có kiểm chứng:

- **Phía người lao động** (`domain_worker_desires.csv`): người trong nghề tự chấm
  *mức độ mong muốn tự động hóa* (1-5) và *thang Human Agency* (HAS, 1-5) cho từng tác vụ.
- **Phía chuyên gia** (`expert_rated_technological_capability.csv`): chuyên gia đánh giá
  *năng lực AI làm được tác vụ đó* (1-5).
- **Danh mục tác vụ** (`task_statement_with_metadata.csv`): mô tả tác vụ theo chuẩn O*NET,
  kèm lương, quy mô việc làm, độ quan trọng.
- **Hồ sơ người lao động** (`domain_worker_metadata.csv`): nhân khẩu + thói quen dùng LLM.

Đối chiếu *muốn* x *làm được* tạo ra **4 vùng tự động hóa (Automation Zones)** - nền tảng
cho mọi khuyến nghị ở cuối.
    """
)

st.subheader("Các trang phân tích")
st.markdown(
    """
1. **Tổng quan** - quy mô dữ liệu, phân bố nghề, chất lượng dữ liệu.
2. **Ma trận Tự động hóa** - Mong muốn x Năng lực AI, 4 vùng ưu tiên.
3. **Human Agency** - người làm CS muốn AI tự chủ tới đâu (H1-H5).
4. **So sánh theo nghề** - nghề nào sẵn sàng cho AI agent nhất.
5. **Người lao động & LLM** - hiện trạng dùng LLM trong công việc CS.
6. **Khuyến nghị** - insight & đề xuất triển khai AI agents.
    """
)

st.info("Dùng menu bên trái để mở từng trang. Bộ lọc nghề áp dụng xuyên suốt.")
st.caption("Phạm vi CS = nhóm O*NET 15-12xx (Computer Occupations) + 11-3021 "
           "(Computer & Information Systems Managers).")
