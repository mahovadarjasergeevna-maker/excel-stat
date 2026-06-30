import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Статистика по Excel", layout="wide")
st.title("Статистика по Excel")
st.caption("Загрузите Excel-файл и получите сводку по городам, руководителям и статусам")

uploaded_file = st.file_uploader("Загрузите Excel файл", type=["xlsx", "xls"])

if uploaded_file is not None:
    xls = pd.ExcelFile(uploaded_file)
    df = pd.read_excel(uploaded_file, sheet_name=xls.sheet_names[0])
    df.columns = [str(c).strip() for c in df.columns]

    required = ["Город", "Руководитель", "Статус", "Физическое лицо"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        st.error("Не найдены столбцы: " + ", ".join(missing))
        st.stop()

    df = df[required].copy()

    df["Город"] = df["Город"].fillna("Не указано")
    df["Руководитель"] = df["Руководитель"].fillna("Не указано")
    df["Статус"] = df["Статус"].fillna("Не указано")
    df["Физическое лицо"] = df["Физическое лицо"].fillna("")

    total = len(df)

    city_stat = df.groupby("Город", as_index=False).size().rename(columns={"size": "Количество"})
    city_stat = city_stat.sort_values("Количество", ascending=False)

    manager_stat = df.groupby("Руководитель", as_index=False).size().rename(columns={"size": "Количество"})
    manager_stat = manager_stat.sort_values("Количество", ascending=False)
    manager_stat["Процент от общего"] = (manager_stat["Количество"] / total * 100).round(1)

    status_stat = df.groupby("Статус", as_index=False).size().rename(columns={"size": "Количество"})
    status_stat = status_stat.sort_values("Количество", ascending=False)

    c1, c2, c3 = st.columns(3)
    c1.metric("Всего сотрудников", total)
    c2.metric("Городов", city_stat.shape[0])
    c3.metric("Руководителей", manager_stat.shape[0])

    st.subheader("По городам")
    fig_city = px.bar(city_stat, x="Город", y="Количество", text="Количество")
    st.plotly_chart(fig_city, use_container_width=True)
    st.dataframe(city_stat, use_container_width=True, hide_index=True)

    st.subheader("По статусам")
    fig_status = px.pie(status_stat, names="Статус", values="Количество", hole=0.4)
    st.plotly_chart(fig_status, use_container_width=True)
    st.dataframe(status_stat, use_container_width=True, hide_index=True)

    st.subheader("По руководителям")
    fig_manager = px.bar(manager_stat.head(20), x="Руководитель", y="Количество", text="Количество")
    st.plotly_chart(fig_manager, use_container_width=True)
    st.dataframe(manager_stat, use_container_width=True, hide_index=True)

    st.subheader("Таблица данных")
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("Сначала загрузите Excel файл.")