import streamlit as st
import pandas as pd
import helpers.data_handling as dh
import plotly.graph_objects as go
from plotly.subplots import make_subplots



country_list = ['at', 'be', 'ch', 'de', 'dk', 'es', 'fr', 'gb', 'ie', 'it', 'lu', 'nl', 'no', 'pt', 'se']


def energy_load_contries_plot():

    selected_countries = st.multiselect(
        'Selected countries',
        country_list,
        country_list[-1])

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


    layout = go.Layout(title='Electric load over time',
                       xaxis=dict(title='time', tickangle=-90),
                       yaxis=dict(title='load'))
    fig = go.Figure(data=traces, layout=layout)
    st.plotly_chart(fig)


def se_weather_and_energy_load_plot():
    weather_df = dh.load_weather_nordics()
    se_weather_df = weather_df[weather_df['country'] == "Sweden"]

    se_load_data = dh.load_country_data('se')
    se_load_data.set_index('date', inplace=True)
    se_load_data = se_load_data['load'].resample('D').mean()
    se_load_data = se_load_data.reset_index()

    merged_load_weather_df = pd.merge(se_load_data, se_weather_df, on="date", how="left")

    x_column = 'date'
    y1_column = 'load'
    y2_column = "tavg"

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=merged_load_weather_df[x_column],
                   y=merged_load_weather_df[y1_column],
                   name=y1_column,
                   marker = {'color' : 'lightblue'}),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=merged_load_weather_df[x_column],
                   y=merged_load_weather_df[y2_column],
                   name=y2_column,
                   marker = {'color' : 'red'}),
        secondary_y=True,
    )

    fig.update_layout(
        title='Load and average temperature over time',
        xaxis_title='Date',
        yaxis=dict(title='Load in MW'),
        yaxis2=dict(title='Temperature in °C'),
    )

    st.plotly_chart(fig)

    corr = merged_load_weather_df[['load', 'tavg']].corr()

    st.text("We can see that energy load and average temperature are negatively correlated.")




st.title('Energy Consumption 2015 - 2020')
energy_load_contries_plot()
se_weather_and_energy_load_plot()


