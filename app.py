"""
Điểm vào (router) dashboard - "Ứng dụng AI Agents trong ngành Khoa học Máy tính".
Môn: Trực quan hóa dữ liệu.  Chạy: streamlit run app.py

Dùng st.navigation để đặt TÊN MENU tiếng Việt CÓ DẤU (thay vì lấy theo tên file).
"""
import streamlit as st

from src import ui

ui.page_config()  # set_page_config + CSS (gọi 1 lần, trước navigation)

pages = [
    st.Page("home.py", title="Trang chủ", icon=":material/home:",
            url_path="trang-chu", default=True),
    st.Page("views/1_Tong_quan.py", title="Tổng quan", icon=":material/dashboard:",
            url_path="tong-quan"),
    st.Page("views/2_Ma_tran_Tu_dong_hoa.py", title="Ma trận Tự động hóa",
            icon=":material/grid_view:", url_path="ma-tran-tu-dong-hoa"),
    st.Page("views/3_Human_Agency.py", title="Human Agency", icon=":material/groups:",
            url_path="human-agency"),
    st.Page("views/4_So_sanh_theo_nghe.py", title="So sánh theo nghề",
            icon=":material/bar_chart:", url_path="so-sanh-theo-nghe"),
    st.Page("views/5_Nguoi_lao_dong_LLM.py", title="Người lao động & LLM",
            icon=":material/smart_toy:", url_path="nguoi-lao-dong-llm"),
    st.Page("views/6_Khuyen_nghi.py", title="Khuyến nghị", icon=":material/lightbulb:",
            url_path="khuyen-nghi"),
]

st.navigation(pages).run()
