"""Trang 6 - Insight & khuyến nghị triển khai AI agents (sinh từ số thật)."""
import streamlit as st

from src import ui
from src import analysis
from src import config

ui.page_config("Khuyến nghị")
ui.hero("Insight & Khuyến nghị triển khai AI Agents",
        "Mọi nhận định sinh từ dữ liệu đang lọc - đổi bộ lọc, con số sẽ cập nhật")

df = ui.sidebar_filter()
k = analysis.kpis(df)
zs = analysis.zone_summary(df)
occ = analysis.occupation_summary(df)

green = analysis.top_tasks(df, config.ZONE_GREEN, 5)
rnd = analysis.top_tasks(df, config.ZONE_RND, 5)
red = analysis.top_tasks(df, config.ZONE_RED, 5)

_REN = {"Task": "Tác vụ", "Occupation": "Nghề", "worker_desire": "Mong muốn",
        "ai_capability": "Năng lực AI", "worker_has": "HAS", "n_workers": "Số người"}

# --- Hiện trạng ---
st.header("Hiện trạng (tóm tắt)")
st.markdown(
    f"""
- Trên **{k['n_tasks']} tác vụ** CS có đủ đánh giá hai phía: mong muốn tự động hóa
  trung bình **{k['mean_desire']}/5**, trong khi năng lực AI (chuyên gia) **{k['mean_cap']}/5**.
  → Chuyên gia đánh giá AI **làm được nhiều hơn** mức người lao động mong muốn.
- **{k['pct_green']}%** tác vụ nằm vùng **Green Light** (vừa muốn, vừa khả thi);
  **{k['pct_red']}%** vùng **Red Light** (AI làm được nhưng người lao động ít muốn).
- Human Agency trung bình **{k['mean_has']}/5**
  ({'nghiêng về giao cho AI làm chính' if k['mean_has'] < 3 else 'nghiêng về giữ vai trò con người'}).
    """
)
cols = st.columns(4)
for col, (_, r) in zip(cols, zs.iterrows()):
    col.metric(r["zone"], f'{r["So task"]} tác vụ', f'{r["Ty le %"]}%')

st.divider()
st.header("Khuyến nghị theo từng vùng")

st.subheader("1) Green Light - triển khai AI agent ngay")
st.markdown("Người lao động muốn & AI đã làm được. Đây là nơi có ROI cao nhất, ít kháng cự.")
st.dataframe(green.rename(columns=_REN).round(2), use_container_width=True, hide_index=True)

st.subheader("2) R&D Opportunity - đầu tư công cụ / mô hình")
st.markdown("Người lao động muốn nhưng AI **chưa** đạt. Đây là hướng đầu tư R&D, "
            "xây agent chuyên biệt cho CS.")
st.dataframe(rnd.rename(columns=_REN).round(2), use_container_width=True, hide_index=True)

st.subheader("3) Red Light - thận trọng, quản trị thay đổi")
st.markdown("AI làm được nhưng người lao động **ít muốn** tự động hóa. Nếu ép buộc sẽ "
            "gây phản kháng → ưu tiên thiết kế 'human-in-the-loop', đào tạo lại.")
st.dataframe(red.rename(columns=_REN).round(2), use_container_width=True, hide_index=True)

st.divider()
st.header("Đề xuất ở cấp nghề")
ready = occ[(occ["mong_muon"] >= config.THRESHOLD) & (occ["nang_luc_AI"] >= config.THRESHOLD)]
caution = occ[(occ["mong_muon"] < config.THRESHOLD) & (occ["nang_luc_AI"] >= config.THRESHOLD)]
st.markdown(
    f"""
- **Sẵn sàng nhất ({len(ready)} nghề):** {', '.join(ready['Occupation'].tolist()) or '(không có theo bộ lọc)'}.
  → Ưu tiên thí điểm (pilot) AI agent ở đây trước.
- **Cần thận trọng ({len(caution)} nghề):** {', '.join(caution['Occupation'].tolist()) or '(không có)'}.
  → AI đủ sức nhưng người lao động dễ kháng cự; triển khai dạng hỗ trợ, minh bạch.
- Thiết kế AI agent theo đúng mức **Human Agency** mà từng nghề mong muốn (xem trang 3),
  thay vì mặc định tự động hóa toàn bộ.
    """
)

st.divider()
st.header("Hạn chế & trung thực dữ liệu")
st.markdown(
    """
- Khảo sát từ tự đánh giá chủ quan (người lao động tự chấm, chuyên gia tự chấm) - không
  phải đo lường năng suất thực tế.
- Chỉ **153 tác vụ CS** có đủ hai phía đánh giá; kết luận giới hạn trong phạm vi này.
- Ngưỡng chia vùng = 3.0 (điểm giữa thang 1-5); đổi ngưỡng sẽ đổi số lượng từng vùng.
- HAS phản ánh **mong muốn**, không phải **khả năng kỹ thuật** giao quyền cho AI.
    """
)
