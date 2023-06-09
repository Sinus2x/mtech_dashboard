import pandas as pd
import streamlit as st
from statistics import proportion_test, plot_ztest, plot_props
from components import load_file, sidebar, solution_description, props_diff

st.session_state['alpha'] = 0.05
st.title('Проверка гипотез')
df = load_file()
with st.expander('Описание решения'):
    solution_description()

if df is not None:
    st.session_state['work_days'], st.session_state['age'] = sidebar(df)
    work_days = st.session_state['work_days']
    age = st.session_state['age']

    # hypothesis 1
    st.subheader('Гипотеза 1')
    men = df[df.sex == 'М']
    men_prop = (men.sick > work_days).mean()

    women = df[df.sex == 'Ж']
    women_prop = (women.sick > work_days).mean()

    z_score, p_val = proportion_test(
        (men.sick > work_days).values,
        (women.sick > work_days).values
    )
    st.session_state['hyp1_z'] = z_score
    st.session_state['hyp1_p'] = p_val
    st.session_state['hyp1_p1'] = men_prop
    st.session_state['hyp1_p2'] = women_prop
    st.session_state['hyp1_name1'] = 'Мужчины'
    st.session_state['hyp1_name2'] = 'Женщины'

    z_dist = plot_ztest('hyp1')
    props = plot_props('hyp1')
    if p_val < st.session_state.alpha:
        if men_prop > women_prop:
            st.session_state['hyp1'] = f'Отклоняем нулевую гипотезу. ' \
                                       f'Мужчины пропускают более {work_days} дней чаще женщин'
        else:
            st.session_state['hyp1'] = f'Отклоняем нулевую гипотезу. ' \
                                       f'Женщины пропускают более {work_days} дней чаще мужчин'
    else:
        st.session_state['hyp1'] = 'Нет оснований отвергать нулевую гипотезу.'

    st.plotly_chart(z_dist)
    st.write(st.session_state['hyp1'])
    props_diff('hyp1')
    st.plotly_chart(props)

    # hypothesis 2
    st.subheader('Гипотеза 2')
    elder = df[df.age > age]
    elder_prop = (elder.sick > work_days).mean()

    junior = df[df.age <= age]
    jun_prop = (junior.sick > work_days).mean()

    z_score, p_val = proportion_test(
        (elder.sick > work_days).values,
        (junior.sick > work_days).values
    )

    st.session_state['hyp2_z'] = z_score
    st.session_state['hyp2_p'] = p_val
    st.session_state['hyp2_p1'] = elder_prop
    st.session_state['hyp2_p2'] = jun_prop
    st.session_state['hyp2_name1'] = f'Старше {age}'
    st.session_state['hyp2_name2'] = f'Младше {age}'

    if p_val < st.session_state.alpha:
        if elder_prop > jun_prop:
            st.session_state['hyp2'] = f'Отклоняем нулевую гипотезу. ' \
                                       f'Старшие сотрудники пропускают более {work_days} дней чаще младших'
        else:
            st.session_state['hyp2'] = f'Отклоняем нулевую гипотезу. ' \
                                       f'Младшие сотрудники пропускают более {work_days} дней чаще старших'
    else:
        st.session_state['hyp2'] = 'Нет оснований отвергать нулевую гипотезу.'

    z_dist = plot_ztest('hyp1')
    props = plot_props('hyp2')

    st.plotly_chart(z_dist)
    st.write(st.session_state['hyp2'])
    props_diff('hyp2')
    st.plotly_chart(props)


