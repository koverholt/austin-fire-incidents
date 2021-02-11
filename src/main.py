import numpy as np
import pandas as pd

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

def apply(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    result = df.to_json(orient="records")
    return (result, 200, headers)
