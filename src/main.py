import numpy as np
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

df = pd.concat(map(pd.read_csv, [
    "https://storage.googleapis.com/austin-fire-incidents/AFD_Fire_Incidents_2013_January_Thru_December.csv",
    "https://storage.googleapis.com/austin-fire-incidents/AFD_Fire_Incidents_2014_January_Thru_December.csv",
    "https://storage.googleapis.com/austin-fire-incidents/AFD_Fire_Incidents_2015_January_Thru_December.csv",
    "https://storage.googleapis.com/austin-fire-incidents/AFD_Fire_Incidents_2016_January_Thru_December.csv",
    "https://storage.googleapis.com/austin-fire-incidents/AFD_Fire_Incidents_2017_January_-_December.csv",
    "https://storage.googleapis.com/austin-fire-incidents/AFD_Fire_Incidents_2018_January_-_December.csv",
]))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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


@app.post("/")
async def get_fire_incidents(request: Request):
    result = df.to_json(orient="records")
    return result
