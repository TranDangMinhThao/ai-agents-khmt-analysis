"""Trang 2 - Ma trận Tự động hóa: Mong muốn (người lao động) x Năng lực AI (chuyên gia)."""
import plotly.express as px
import streamlit as st

from src import ui
from src import analysis
from src import config

ui.page_config("Ma trận Tự động hóa")
ui.hero("Ma trận Tự động hóa", "Mong muốn (người lao động) x Năng lực AI (chuyên gia) - ngưỡng chia vùng = 3.0")

df = ui.sidebar_filter()

# --- Tóm tắt 4 vùng ---
zs = analysis.zone_summary(df)
cols = st.columns(4)
for col, (_, row) in zip(cols, zs.iterrows()):
    col.metric(row["zone"], f'{row["So task"]} tác vụ', f'{row["Ty le %"]}%')

st.divider()

# --- Scatter ---
fig = px.scatter(
    df, x="ai_capability", y="worker_desire", color="zone",
    color_discrete_map=config.ZONE_COLOR, size="n_workers",
    hover_data={"Task": True, "Occupation": True, "worker_desire": ":.2f",
                "ai_capability": ":.2f", "n_workers": True},
    labels={"ai_capability": "Năng lực AI (chuyên gia, 1-5)",
            "worker_desire": "Mong muốn tự động hóa (người lao động, 1-5)", "zone": "Vùng"},
    category_orders={"zone": config.ZONE_ORDER},
)
fig.add_hline(y=config.THRESHOLD, line_dash="dash", line_color="#888")
fig.add_vline(x=config.THRESHOLD, line_dash="dash", line_color="#888")
fig.update_layout(height=600, legend=dict(orientation="h", y=1.08),
                  margin=dict(l=10, r=10, t=10, b=10))
fig.add_annotation(x=4.5, y=4.7, text="Green Light", showarrow=False, font=dict(color=config.ZONE_COLOR[config.ZONE_GREEN]))
fig.add_annotation(x=1.5, y=4.7, text="R&D Opportunity", showarrow=False, font=dict(color=config.ZONE_COLOR[config.ZONE_RND]))
fig.add_annotation(x=4.5, y=1.3, text="Red Light", showarrow=False, font=dict(color=config.ZONE_COLOR[config.ZONE_RED]))
fig.add_annotation(x=1.5, y=1.3, text="Low Priority", showarrow=False, font=dict(color=config.ZONE_COLOR[config.ZONE_LOW]))
st.plotly_chart(fig, use_container_width=True)

with st.expander("Ý nghĩa 4 vùng"):
    zsv = zs.rename(columns={"zone": "Vùng", "So task": "Số tác vụ", "Ty le %": "Tỷ lệ %",
                             "Mo ta": "Mô tả"})
    st.dataframe(zsv[["Vùng", "Số tác vụ", "Tỷ lệ %", "Mô tả"]], use_container_width=True,
                 hide_index=True)

st.divider()
st.subheader("Top tác vụ theo từng vùng")
zone = st.selectbox("Chọn vùng", config.ZONE_ORDER, index=0)
st.caption(config.ZONE_DESC[zone])
tt = analysis.top_tasks(df, zone, n=12)
tt = tt.rename(columns={"Task": "Tác vụ", "Occupation": "Nghề", "worker_desire": "Mong muốn",
                        "ai_capability": "Năng lực AI", "worker_has": "Human Agency",
                        "n_workers": "Số người chấm"})
st.dataframe(tt.round(2), use_container_width=True, hide_index=True)
