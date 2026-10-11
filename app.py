import pandas as pd
import streamlit as st

st.set_page_config(page_title="Quản lý điểm sinh viên", layout="wide")

# ---------- Hàm xử lý ----------
def tinh_tong_ket(cc, gk, ck):
    """Tổng kết = 10% chuyên cần + 30% giữa kỳ + 60% cuối kỳ."""
    return round(cc * 0.1 + gk * 0.3 + ck * 0.6, 2)


def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    if diem >= 7.0:
        return "Khá"
    if diem >= 5.0:
        return "Trung bình"
    return "Yếu"


# ---------- Dữ liệu 10 sinh viên ----------
data = [
    ("Nguyễn Văn An", 9, 8.0, 8.5),
    ("Trần Thị Bình", 10, 7.5, 9.0),
    ("Lê Hoàng Cường", 8, 6.0, 7.0),
    ("Phạm Thu Dung", 9, 9.0, 9.5),
    ("Võ Minh Em", 7, 5.0, 4.5),
    ("Đặng Quốc Phong", 8, 6.5, 6.0),
    ("Huỳnh Ngọc Giàu", 10, 8.5, 8.0),
    ("Bùi Thanh Hà", 6, 4.0, 3.5),
    ("Ngô Gia Huy", 9, 7.0, 7.5),
    ("Lý Kim Khánh", 8, 7.5, 8.0),
]

df = pd.DataFrame(data, columns=["Họ tên", "Chuyên cần", "Giữa kỳ", "Cuối kỳ"])
df["Tổng kết"] = df.apply(
    lambda r: tinh_tong_ket(r["Chuyên cần"], r["Giữa kỳ"], r["Cuối kỳ"]), axis=1
)
df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# ---------- Giao diện ----------
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

st.subheader("Bảng điểm 10 sinh viên")
st.dataframe(df, use_container_width=True, hide_index=True)

# Thống kê
st.subheader("Thống kê")
col1, col2, col3, col4 = st.columns(4)

diem_tb = df["Tổng kết"].mean()
sv_cao = df.loc[df["Tổng kết"].idxmax()]
sv_thap = df.loc[df["Tổng kết"].idxmin()]
so_dat = int((df["Tổng kết"] >= 5).sum())

col1.metric("Điểm trung bình lớp", f"{diem_tb:.2f}")
col2.metric("Cao nhất", f"{sv_cao['Tổng kết']}", sv_cao["Họ tên"], delta_color="off")
col3.metric("Thấp nhất", f"{sv_thap['Tổng kết']}", sv_thap["Họ tên"], delta_color="off")
col4.metric("Số sinh viên đạt", f"{so_dat}/{len(df)}")

# Chọn sinh viên
st.subheader("Tra cứu sinh viên")
ten = st.selectbox("Chọn sinh viên:", df["Họ tên"])
sv = df[df["Họ tên"] == ten].iloc[0]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Chuyên cần", sv["Chuyên cần"])
c2.metric("Giữa kỳ", sv["Giữa kỳ"])
c3.metric("Cuối kỳ", sv["Cuối kỳ"])
c4.metric("Điểm tổng kết", sv["Tổng kết"])
c5.metric("Xếp loại", sv["Xếp loại"])

# Biểu đồ
st.subheader("Biểu đồ điểm tổng kết")
st.bar_chart(df.set_index("Họ tên")["Tổng kết"])

# Chân trang
st.markdown("---")
st.caption("Người tạo ứng dụng: [HỌ TÊN CỦA BẠN] - MSSV: [MSSV CỦA BẠN]")
