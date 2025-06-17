
import streamlit as st
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
import pandas as pd
import re

def extract_age_gender_data(image):
    text = pytesseract.image_to_string(image)
    matches = re.findall(r'(\d{2}-\d{2}|\d{2}\+)[^\d]*(\d+%)?[^\d]*(\d+%)?', text)
    data = []
    for match in matches:
        age_range = match[0]
        percents = [p for p in match[1:] if p]
        male, female = (percents + [None, None])[:2]
        data.append((age_range, male, female))
    df = pd.DataFrame(data, columns=["Age Range", "Male %", "Female %"])
    return df

def extract_country_data(image):
    text = pytesseract.image_to_string(image)
    matches = re.findall(r'([A-Za-z ]+)\s+(\d+\.\d+%)', text)
    df = pd.DataFrame(matches, columns=["Country", "Audience %"])
    return df

st.title("HypeAuditor Rapor Verisi Çıkarıcı")
st.markdown("Yalnızca oranları ve yerleşimleri sabit olan ekran görüntülerini yükleyiniz.")

uploaded_proje1 = st.file_uploader("Proje 1: Yaş ve Cinsiyet Grafiği (Bar chart olan)", type=["png", "jpg", "jpeg"], key="proje1")
uploaded_proje2 = st.file_uploader("Proje 2: Ülke ve İzleyici Oranı Tablosu", type=["png", "jpg", "jpeg"], key="proje2")

if uploaded_proje1 and uploaded_proje2:
    with st.spinner("Veriler çıkarılıyor..."):
        img1 = Image.open(uploaded_proje1)
        age_gender_df = extract_age_gender_data(img1)

        img2 = Image.open(uploaded_proje2)
        country_df = extract_country_data(img2)

        st.subheader("Yaş Aralığı ve Cinsiyet Verisi")
        st.dataframe(age_gender_df)
        csv1 = age_gender_df.to_csv(index=False).encode("utf-8")
        st.download_button("Yaş-Cinsiyet CSV İndir", csv1, "yas_cinsiyet.csv")

        st.subheader("Ülke ve İzleyici Oranı Verisi")
        st.dataframe(country_df)
        csv2 = country_df.to_csv(index=False).encode("utf-8")
        st.download_button("Ülke CSV İndir", csv2, "ulke_oran.csv")

elif uploaded_proje1 or uploaded_proje2:
    st.info("Lütfen her iki ekran görüntüsünü de yükleyiniz.")
