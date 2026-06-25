"""
Cau hinh trung tam cho dashboard "Ung dung AI Agents trong nganh Khoa hoc May tinh".

Moi dinh nghia pham vi (scope), nguong (threshold), nhan (label) deu o day de
tai tao duoc va de bao ve truoc thay. KHONG hard-code rai rac trong cac trang.
"""
from pathlib import Path

# --- Duong dan ---
ROOT = Path(__file__).resolve().parent.parent
DATA = {
    "desires": ROOT / "domain_worker_desires.csv",
    "expert": ROOT / "expert_rated_technological_capability.csv",
    "tasks": ROOT / "task_statement_with_metadata.csv",
    "metadata": ROOT / "domain_worker_metadata.csv",
}

# --- Pham vi "Khoa hoc May tinh" (co can cu, KHONG gom bua) ---
# Nhom O*NET 15-12xx = "Computer Occupations" + 11-3021 (Computer & Information
# Systems Managers, vai tro quan ly nhung dac thu CNTT). Loc theo MA SOC, khong
# theo tu khoa ten -> tranh dinh nham (vd "Data Entry Keyers" 43-9021 KHONG phai CS).
def is_cs_code(code: str) -> bool:
    code = (code or "").strip()
    return code.startswith("15-12") or code == "11-3021.00"

# --- Thang do (da verify: tat ca rating la so nguyen 1..5) ---
RATING_MIN, RATING_MAX = 1, 5
THRESHOLD = 3.0  # diem giua thang 1..5; >=3 = "cao", <3 = "thap"

# --- 4 vung tu dong hoa (Automation Zones): Desire (worker) x Capability (expert) ---
# Y tuong: doi chieu "nguoi lao dong CO MUON tu dong hoa" voi "AI CO LAM DUOC".
ZONE_GREEN = "Green Light"          # muon cao + AI lam duoc cao  -> trien khai AI agent ngay
ZONE_RND = "R&D Opportunity"        # muon cao + AI chua lam duoc  -> co hoi dau tu R&D
ZONE_RED = "Red Light"              # muon thap + AI lam duoc cao  -> tu dong hoa nhung nguoi lao dong de khang
ZONE_LOW = "Low Priority"           # muon thap + AI chua lam duoc -> uu tien thap

ZONE_ORDER = [ZONE_GREEN, ZONE_RND, ZONE_RED, ZONE_LOW]
ZONE_DESC = {
    ZONE_GREEN: "Muốn cao & AI làm được cao - triển khai AI agent ngay (ưu tiên #1)",
    ZONE_RND: "Muốn cao & AI chưa làm được - cơ hội đầu tư R&D / công cụ",
    ZONE_RED: "Muốn thấp & AI làm được cao - cảnh báo: ép tự động hóa dễ gây phản kháng",
    ZONE_LOW: "Muốn thấp & AI chưa làm được - ưu tiên thấp, giữ nguyên lao động người",
}
ZONE_COLOR = {
    ZONE_GREEN: "#2e9e5b",
    ZONE_RND: "#2f6fed",
    ZONE_RED: "#e0563b",
    ZONE_LOW: "#9aa0a6",
}

def classify_zone(desire: float, capability: float) -> str:
    hi_d = desire >= THRESHOLD
    hi_c = capability >= THRESHOLD
    if hi_d and hi_c:
        return ZONE_GREEN
    if hi_d and not hi_c:
        return ZONE_RND
    if (not hi_d) and hi_c:
        return ZONE_RED
    return ZONE_LOW

# --- Human Agency Scale (HAS H1..H5) ---
# Thang do muc do con nguoi muon giu vai tro khi AI tham gia tac vu.
HAS_LABEL = {
    1: "H1 - AI làm toàn bộ (không cần người)",
    2: "H2 - AI làm chính, người giám sát nhẹ",
    3: "H3 - Đối tác ngang hàng (người + AI)",
    4: "H4 - Người làm chính, AI hỗ trợ",
    5: "H5 - Con người làm toàn bộ (AI tối thiểu)",
}
HAS_COLOR = ["#1a7f37", "#3fb950", "#d4a72c", "#e08a3b", "#cf222e"]

# --- Bang mau chung ---
COLOR_WORKER = "#2f6fed"   # mong muon cua nguoi lao dong
COLOR_EXPERT = "#e0563b"   # nang luc AI do chuyen gia danh gia
COLOR_ACCENT = "#7c4dff"
