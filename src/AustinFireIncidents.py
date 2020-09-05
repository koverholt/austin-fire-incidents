import Algorithmia
import numpy as np
import pandas as pd

client = Algorithmia.client("simSSc1M+5bDh1CtJ/qnBs0SBba1")

df = pd.concat(map(pd.read_csv, [
    client.file("data://koverholt/AustinFireIncidents/AFD_Fire_Incidents_2013_January_Thru_December.csv").getFile(),
    client.file("data://koverholt/AustinFireIncidents/AFD_Fire_Incidents_2014_January_Thru_December.csv").getFile(),
    client.file("data://koverholt/AustinFireIncidents/AFD_Fire_Incidents_2015_January_Thru_December.csv").getFile(),
    client.file("data://koverholt/AustinFireIncidents/AFD_Fire_Incidents_2016_January_Thru_December.csv").getFile(),
    client.file("data://koverholt/AustinFireIncidents/AFD_Fire_Incidents_2017_January_-_December.csv").getFile(),
    client.file("data://koverholt/AustinFireIncidents/AFD_Fire_Incidents_2018_January_-_December.csv").getFile(),
]))

df[["Latitude", "Longitude"]] = df["Location 1"].str.split(", ", expand=True)

df["Latitude"] = df["Latitude"].str.strip("()")
df["Longitude"] = df["Longitude"].str.strip("()")

df["Latitude"] = df["Latitude"].map(lambda x: "{:.0f}".format(float(x)))
df["Longitude"] = df["Longitude"].map(lambda x: "{:.0f}".format(float(x)))

df["Latitude"] = df["Latitude"].replace("nan", np.nan)
df["Longitude"] = df["Longitude"].replace("nan", np.nan)

df = df.dropna(subset=["Latitude", "Longitude"])

df["Latitude"] = df["Latitude"].astype(int) / 1000000
df["Longitude"] = df["Longitude"].astype(int) / -1000000


def apply(input):
    return df.to_json(orient="records")
