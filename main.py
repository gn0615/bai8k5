import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. Chuẩn bị dữ liệu (Đã sửa lỗi dấu chấm ở dòng 1 và 5)
csv_data = '''id kh,tuoi,gioi tinh,thu nhap,nghe,diem tin dung,sp da mua,gia,so luong,ngay mua
1,30,nam,50000,ky su phan mem,750,dien thoai,5000,1,2026-02-15
2,25,nu,30000,giao vien,680,may tinh,700,1,2026-01-10
3,40,nam,75000,bac si,820,tivi,1000,1,2026-03-02
4,50,nu,0,chu doanh nghiep,700,tu lanh,1200,2,2026-01-28
5,60,nam,60000,nghi huu,800,may giat,1500,1,2026-01-30
'''

with open('bai8.csv', 'w', encoding='utf-8') as f:
    f.write(csv_data)

# 2. Đọc dữ liệu
df = pd.read_csv('bai8.csv')

st.title('Phân tích dữ liệu khách hàng')
st.subheader('Dữ liệu gốc:')
st.dataframe(df)

# 3. Phân tích logic bằng code
roi_bo = df[df['diem tin dung'] <= 700]['id kh'].tolist()
mua_hang = df[(df['thu nhap'] >= 50000) & (df['diem tin dung'] >= 750)]['id kh'].tolist()
chi_tieu = df[df['nghe'].isin(['bac si', 'chu doanh nghiep'])]['id kh'].tolist()

st.subheader('Kết quả phân tích logic')
st.write(f'**Khách hàng có khả năng rời bỏ:** {roi_bo}')
st.write(f'**Khách hàng tiềm năng mua thêm:** {mua_hang}')
st.write(f'**Khách hàng có khả năng chi tiêu cao:** {chi_tieu}')

# 4. Phân tích bằng AI (Gemini)
try:
    # Lấy API Key từ secrets
    genai.configure(api_key=st.secrets['gg_api'])
    model = genai.GenerativeModel('gemini-1.5-flash') # Dùng bản 1.5 ổn định

    p = f"""Đây là dữ liệu khách hàng: 
    {df.to_string()}
    
    Hãy phân tích hành vi khách hàng dựa trên thu nhập, nghề nghiệp và điểm tín dụng. 
    Đưa ra ít nhất 3 insight quan trọng và đề xuất hành động (viết khoảng 200-300 từ).
    """

    if st.button('Chạy phân tích AI'):
        with st.spinner('Đang đợi Gemini trả lời...'):
            r = model.generate_content(p)
            st.subheader("Insight từ AI (Gemini)")
            st.write(r.text)
except Exception as e:
    st.error(f"Lỗi cấu hình AI hoặc API Key: {e}")
