import requests

YOUR_HASH_PASSWD = "51a135add736e302e3337f3f79823413105e75ba33cecf66d1e5f76bc3e5ea16"

data = {
    "passwd": YOUR_HASH_PASSWD,
    "values": {
        "date": "2025-03-15",
        "time": "16:30:00",
        "indoor_temp": 15,
        "indoor_humidity": 70
    }
}

response = requests.post("https://weather-station-app-691588068776.europe-west6.run.app/send-to-bigquery", json=data)
print(response.status_code, response.text)
