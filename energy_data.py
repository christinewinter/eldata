import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import helpers.data_handling as dh
import plotly.express as px

country_list = ['at', 'be', 'ch', 'de', 'dk', 'es', 'fr', 'gb', 'ie', 'it', 'lu', 'nl', 'no', 'pt', 'se']


def interactive_plot():

    col1, col2, col3 = st.columns(3)
    country = col1.selectbox('Select the country', options=country_list)

    df = dh.load_country_data(country)
    start_dt = st.sidebar.date_input('Start date', value=df['time'].min())
    end_dt = st.sidebar.date_input('End date', value=df['time'].max())

    df = df[(df['time'] > pd.Timestamp(start_dt, tz="utc"))
            & (df['time'] < pd.Timestamp(end_dt, tz="utc"))]

    plot = px.line(df, x='time', y='load')
    st.plotly_chart(plot, use_container_width=True)


    # TODO plot moving average
    # TODO time range selection


st.title('Energy Consumption 2015 - 2020')


interactive_plot()


