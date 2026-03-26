cav_data = '''id kh,tuoi,gioi tinh,thu nhap,nghe,diem tin dung,sp da mua,gia,so luong,ngay mua
1,30,nam,50000.ky su phan mem,750,dien thoai,5000,1,2026-02-15
2,25,nu,30000,giao vien,680,may tinh,700,1,2026-01-10
3,40,nam,75000,bac si,820,tivi,1000,1,2026-03-02
4,50,nu,,chu doanh nghiep,700,tu lanh,1200,2,2026-01-28
5,60,nam.60000,nghi huu,800,may giat,1500,1,2026-01-30
'''
with open('bai8.csv','w',encoding='utf-8') as f: f.write(csv_data)
import streamlit as st, pandas as pd
df = pd.read_cvs('bai8.csv')
st.title('phan tich dl khach hang')
st,subheader('dl goc:')
st.dataframe(df)


roi_bo = df[df['diem tin dung'] <= 700]['id kh'].tolist()
mua_hang = df[(df['thu nhap'] >= 50000) & (df['diem tin dung'] >= 750)]['id kh'].tolist()
chi_tieu = df[df['nghe'].isin(['bac si','chu doanh nghiep'])]['id kh'].tolist()

st.subhesder('kq phan tich')
st.write('kh co kha nang roi bo:',roi_bo)
st.write('kh co kha nang mua hang thang toi',mua_hang)
st.write('kh co kha nang chi tieu nhieu hon',chi_tieu)

import google.generativeai as genai
genai.configure(api_key=st.secrets['gg_api'])
model = genai.GenerativeModel('gemini-2.5-flash')
p = f"""Đây là dữ liệu khách hàng: {df.to_string()}
Hãy phân tích hành vi khách hàng và đưa ra insight quan trọng (200-300 từ).
"""
r = model.ganerate_content(p)
st.subheader("Phân tích từ AI (Gemini)")
st.write(r.text)
