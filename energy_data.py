import streamlit as st
import pandas as pd
import helpers.data_handling as dh
import plotly.express as px
import plotly.graph_objects as go


country_list = ['at', 'be', 'ch', 'de', 'dk', 'es', 'fr', 'gb', 'ie', 'it', 'lu', 'nl', 'no', 'pt', 'se']


def interactive_plot():

    selected_countries = st.multiselect(
        'Selected countries',
        country_list,
        country_list[0])

    col2, col3 = st.columns(2)

    start_dt = col2.date_input('Start date', value=dh.STUDY_START_DATE)
    end_dt = col3.date_input('End date', value=dh.STUDY_END_DATE)

    df_list = []
    for country in selected_countries:
        df = dh.load_country_data(country)  # Replace with the appropriate way to load your data frame
        df = df[(df['time'] > pd.Timestamp(start_dt, tz="utc"))
                & (df['time'] < pd.Timestamp(end_dt, tz="utc"))]
        df_list.append(df)

    traces = []
    for i, df in enumerate(df_list):
        trace = go.Scatter(x=df['time'], y=df['load'], name=selected_countries[i])
        traces.append(trace)


    layout = go.Layout(title='Energy load over time',
                       xaxis=dict(title='time', tickangle=-90),
                       yaxis=dict(title='load'))
    fig = go.Figure(data=traces, layout=layout)
    st.plotly_chart(fig)


st.title('Energy Consumption 2015 - 2020')
interactive_plot()


