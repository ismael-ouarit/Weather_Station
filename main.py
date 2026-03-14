#%%
from flask import Flask, request
import os
from google.cloud import bigquery
import requests
from datetime import datetime

# You only need to uncomment the line below if you want to run your flask app locally.
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path-to-service-account-key-json"
client = bigquery.Client(project="weather-station-490015", location="europe-west6")

#%%

# For authentication

YOUR_HASH_PASSWD = "51a135add736e302e3337f3f79823413105e75ba33cecf66d1e5f76bc3e5ea16" # YOUR_HASH_PASSWD

app = Flask(__name__)

# OpenWeather API config
API_KEY = "e745148a9822f0136e732477cac53d64"
CITY = "Lausanne"
WEATHER_URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def get_outdoor_data():
    response = requests.get(WEATHER_URL)
    weather_data = response.json()
    return {
        "outdoor_temp": weather_data["main"]["temp"],
        "outdoor_humidity": weather_data["main"]["humidity"],
        "outdoor_weather": weather_data["weather"][0]["description"]
    }

# get the column names of the db
q = """
SELECT * FROM `weather-station-490015.IoT_Dataset.weather-records` LIMIT 10
"""
query_job = client.query(q)
df = query_job.to_dataframe()
#%%
@app.route('/send-to-bigquery', methods=['GET', 'POST'])
def send_to_bigquery():
    if request.method == 'GET':
        return get_outdoor_data()

    if request.method == 'POST':
        if request.get_json(force=True)["passwd"] != YOUR_HASH_PASSWD:
            raise Exception("Incorrect Password!")
        data = request.get_json(force=True)["values"]
        # For exercise 2: Call the openweatherapi and add the resulting 
        # values to the `data` dictionary
        data.update(get_outdoor_data())
        # building the query
        q = """INSERT INTO `weather-station-490015.IoT_Dataset.weather-records` 
        """
        names = """"""
        values = """"""
        for k, v in data.items():
            names += f"""{k},"""
            if df.dtypes[k] == float:
                values += f"""{v},"""
            else:
                # string values in the query should be in single qutation!
                values += f"""'{v}',"""
        # remove the last comma
        names = names[:-1]
        values = values[:-1]
        q = q + f""" ({names})""" + f""" VALUES({values})"""
        query_job = client.query(q)
        return {"status": "sucess", "data": data}
    return {"status": "failed"}
        


@app.route('/get_outdoor_weather', methods=['GET', 'POST'])
def get_outdoor_weather():
    if request.method == 'POST':
        if request.get_json(force=True)["passwd"] != YOUR_HASH_PASSWD:
            raise Exception("Incorrect Password!")
        # get the latest outdoor temp values from the db
        q = """
        SELECT * FROM `weather-station-490015.IoT_Dataset.weather-records` ORDER BY date DESC LIMIT 1
        """
        query_job = client.query(q)
        df = query_job.to_dataframe()
        return df.to_dict(orient='records')[0]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


