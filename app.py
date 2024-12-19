import streamlit as st
import pandas as pd

# Загрузка данных
@st.cache
def load_data():
    return pd.read_csv('data.csv')

data = load_data()

# Заголовок приложения
st.title("Анализ данных пассажиров Титаника")
st.write("Интерактивное приложение для анализа данных Титаника.")

# Выбор задачи
task = st.selectbox(
    "Выберите задание",
    options=[
        "Диапазон возрастов (min и max)",
        "Количество спасенных и погибших по пункту посадки",
        "Процент выживших молодых и старых пассажиров"
    ]
)

# Реализация задач
if task == "Диапазон возрастов (min и max)":
    gender = st.selectbox("Выберите пол", options=['male', 'female'])
    survived = st.radio("Спасен или погиб?", options=[0, 1])
    filtered_data = data[(data['Sex'] == gender) & (data['Survived'] == survived)]
    if not filtered_data.empty:
        st.write(f"Минимальный возраст: {filtered_data['Age'].min()}")
        st.write(f"Максимальный возраст: {filtered_data['Age'].max()}")
    else:
        st.write("Нет данных для выбранных условий.")
elif task == "Количество спасенных и погибших по пункту посадки":
    embarked = st.selectbox("Выберите пункт посадки", options=data['Embarked'].dropna().unique())
    result = data[data['Embarked'] == embarked]['Survived'].value_counts()
    st.write(f"Спасенные: {result.get(1, 0)}, Погибшие: {result.get(0, 0)}")
elif task == "Процент выживших молодых и старых пассажиров":
    ticket_class = st.selectbox("Выберите класс билета", options=data['Pclass'].unique())
    young = data[(data['Pclass'] == ticket_class) & (data['Age'] < 30)]
    old = data[(data['Pclass'] == ticket_class) & (data['Age'] > 60)]
    st.write(f"Процент выживших молодых: {young['Survived'].mean() * 100:.2f}%")
    st.write(f"Процент выживших старых: {old['Survived'].mean() * 100:.2f}%")
