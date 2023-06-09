import numpy as np
import pandas as pd
import streamlit as st
from typing import Literal

def load_file():
    uploaded_file = st.file_uploader('Загрузи данные о сотрудниках')
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        df.rename({
            'Количество больничных дней': 'sick',
            'Возраст': 'age',
            'Пол': 'sex'
        }, axis=1, inplace=True)
        return df
    return None


def sidebar(df: pd.DataFrame):
    with st.sidebar:

        work_days = st.select_slider(
            'Выбери параметр work_days',
            np.arange(df.sick.min() + 1, df.sick.max() - 1)
        )

        age = st.select_slider(
            'Выбери параметр age',
            np.arange(df.age.min() + 1, df.age.max() - 1)
        )
    return work_days, age


def solution_description():
    st.markdown(
        'Подход для проверки 2-х гипотез будет следующим. Будем сравнивать доли $p$ успехов в двух группах.\
         Для первой гипотезы группами будут сотрудники мужского и женского пола, \
         а для второй - работники старше $age$ и младше $age$ лет. Успехом будет событие\
          "сотрудник пропустил больше $work\_days$ дней"'
    )
    st.markdown(
        r'Будем делать правосторонний тест, если $\hat{p_1} > \hat{p_2}$ (доли, посчитанные по выборке), \
        и левосторонний - в противном случае.'
    )
    st.subheader('Гипотеза 1')
    st.markdown(
        r'Пусть $p_1$ - доля мужчин, пропускающих более $work\_days$ в течение года, '
        r'а $p_2$ - доля женщин.$\\H_0: p_1 = p_2\\H_1: p_1 > p_2$'
    )

    st.subheader('Гипотеза 2')
    st.markdown(
        r'Пусть $p_1$ - доля работников старше $age$, пропускающих более $work\_days$ в течение года,'
        r' а $p_2$ - доля сотрудников младше $age$, пропускающих более $work\_days$ в течение года.'
        r'$\\H_0: p_1 = p_2\\H_1: p_1 > p_2$'
    )

    st.subheader('Процедура проверки гипотез')
    st.markdown(
        'В каждой гипотезе у нас есть две независимые выборки объёма $n_1$ и $n_2$ из "успехов" или "неуспехов". '
        'Будем использовать **z-test**:'
        r'$\\X_1 = (X_{11}, ..., X_{1n_1}), X_{1i} \sim Ber(p_1)'
        r'\\X_2 = (X_{21}, ..., X_{2n_2}), X_{2i} \sim Ber(p_2)\\$'
        'Пусть в 1-й выборке $m_1$ успехов, а во 2-й выборке - $m_2$. Тогда: '
        r'$\\\hat{p_1} = \frac{m_1}{n_1}, \hat{p_2} = \frac{m_2}{n_2} \\$'
        'По ЦПТ:'
        r'$\\\hat{p_1} \sim N(p_1, \frac{p_1(1-p_1)}{n_1}) \\'
        r'\hat{p_2} \sim N(p_2, \frac{p_2(1-p_2)}{n_2}) \\'
        r'\hat{p_1} - \hat{p_2} \sim N(p_1 - p_2, \frac{p_1(1-p_1)}{n_1} + \frac{p_2(1-p_2)}{n_2})$'
    )

    st.markdown(
        'При верной $H_0: '
        r'\\Z = \frac{\hat{p_1} - \hat{p_2}}{\sqrt{P(1 - P)(\frac{1}{n_1} + \frac{1}{n_2})}} \sim N(0, 1),'
        r' P = \frac{m_1 + m_2}{n_1 + n_2}$'
    )


def props_diff(hypothesis: Literal['hyp1', 'hyp2']):
    with st.container():
        col1, col2 = st.columns([1, 1])
        prop1 = st.session_state[f'{hypothesis}_p1']
        prop2 = st.session_state[f'{hypothesis}_p2']
        p = st.session_state[f'{hypothesis}_p']
        delta = round((prop2 - prop1) / (prop1 + 1e-7) * 100, 2)
        col1.metric(label='Разница между долями в первой и второй группе', value=f'{delta} %', delta=f'{delta} %')
        significance = 'Да' if p < st.session_state.alpha else 'Нет'
        col2.metric(label='Стат. значима ?', value=significance)
