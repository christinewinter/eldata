import pandas as pd

STUDY_START_DATE = pd.Timestamp("2015-01-01 00:00", tz="utc")
STUDY_END_DATE = pd.Timestamp("2020-01-31 23:00", tz="utc")
LOAD_DATA_PATH = "data/western-europe/"
WEATHER_DATA_PATH = "data/weather-nordics/nordics_weather.csv"

def load_country_data(country_code):
    df = pd.read_csv(LOAD_DATA_PATH + country_code + ".csv")
    df = df.drop(columns="end").set_index("start")
    df.index = pd.to_datetime(df.index)
    df.index.name = "time"
    df = df.groupby(pd.Grouper(freq="h")).mean()
    df = df.loc[(df.index >= STUDY_START_DATE) & (df.index <= STUDY_END_DATE), :]
    df = df.reset_index()
    df = df.dropna()
    df['date'] = pd.to_datetime(df['time'].dt.date, format='%Y-%m-%d')

    return df

def load_multiple_countries(country_codes):

    dfs = []

    for country_code in country_codes:
        df = load_country_data(country_code)
        df['country'] = country_code
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


def load_weather_nordics():
    weather_df = pd.read_csv(WEATHER_DATA_PATH)
    weather_df['date'] = pd.to_datetime(weather_df['date'], format='%m/%d/%Y')
    return weather_df
