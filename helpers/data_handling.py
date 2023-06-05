import pandas as pd
import numpy as np
import math

STUDY_START_DATE = pd.Timestamp("2015-01-01 00:00", tz="utc")
STUDY_END_DATE = pd.Timestamp("2020-01-31 23:00", tz="utc")
DATA_PATH = "//data/western-europe/"


def load_country_data(country_code):
    df = pd.read_csv(DATA_PATH + country_code + ".csv")
    df = df.drop(columns="end").set_index("start")
    df.index = pd.to_datetime(df.index)
    df.index.name = "time"
    df = df.groupby(pd.Grouper(freq="h")).mean()
    df = df.loc[(df.index >= STUDY_START_DATE) & (df.index <= STUDY_END_DATE), :]
    df = df.reset_index()
    df = df.dropna()

    return df
