import numpy as np
import scipy.stats as stats
import plotly.graph_objects as go
import streamlit as st
from typing import Literal


def proportion_test(x1: np.ndarray, x2: np.ndarray):
    """
    Проверяем, есть ли стат. значимая разница между долями
    Используем односторонний критерий, т.к. важен знак разницы
    """
    m1 = np.sum(x1)
    m2 = np.sum(x2)
    n1 = len(x1)
    n2 = len(x2)
    p1 = m1 / n1
    p2 = m2 / n2
    p = (m1 + m2) / (n1 + n2)
    z_score = abs(p1 - p2) / np.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))

    # в зависимости от знака p1 - p2
    # получаем либо левый, либо правый хвост распределения
    p_val = stats.norm.sf(z_score)
    return z_score, p_val


def plot_ztest(
    hypothesis: Literal['hyp1', 'hyp2']
):
    prop1 = st.session_state[f'{hypothesis}_p1']
    prop2 = st.session_state[f'{hypothesis}_p2']
    z_score = st.session_state[f'{hypothesis}_z']
    p_val = st.session_state[f'{hypothesis}_p']
    alpha = st.session_state.alpha
    # Create a standard normal distribution
    x = np.linspace(-4, 4, 100)
    y = 1 / np.sqrt(2 * np.pi) * np.exp(-x**2 / 2)

    z = z_score if prop1 > prop2 else -z_score
    crit = stats.norm.ppf(1 - alpha) if z > 0 else stats.norm.ppf(alpha)
    to_fill = (x >= crit) if z > 0 else (x <= crit)

    # Create a trace for the standard normal distribution
    trace_normal = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='Standard Normal Distribution'
    )

    # Create the figure
    fig = go.Figure(
        data=[trace_normal],
        layout=dict(
            title='Результаты z-теста',
            xaxis=dict(title='z-score'),
            yaxis=dict(title='Probability Density')
        )
    )

    trace_crit = go.Scatter(
        x=x[to_fill],
        y=y[to_fill],
        fill='tozeroy',
        mode='none',
        name='p < alpha',
        fillcolor='red',
    )

    z_trace = go.Scatter(
        x=[z],
        y=[stats.norm.pdf(z)],
        mode='markers',
        name='z_score',
        marker=dict(
            color='black',
            size=10
        ),
        customdata=[['{:.3f}'.format(p_val)]],
        hovertemplate='z_score: %{x}<br>p: %{customdata[0]}'
    )

    fig.add_trace(trace_crit)
    fig.add_trace(z_trace)
    return fig


def plot_props(
        hypothesis: Literal['hyp1', 'hyp2']
):
    work_days = st.session_state.work_days
    name1 = st.session_state[f'{hypothesis}_name1']
    name2 = st.session_state[f'{hypothesis}_name2']
    prop1 = st.session_state[f'{hypothesis}_p1']
    prop2 = st.session_state[f'{hypothesis}_p2']
    title = f'Доли сотрудников, пропустивших больше {work_days} дней'
    fig = go.Figure(
        layout=dict(
            title=title,
            xaxis=dict(title='Группа'),
            yaxis=dict(title=f'Доля')
        )
    )

    fig.add_trace(go.Bar(
        x=[name1, name2],
        y=[prop1, prop2],
        showlegend=False
    ))
    return fig
