import requests

YOUR_HASH_PASSWD = "51a135add736e302e3337f3f79823413105e75ba33cecf66d1e5f76bc3e5ea16"

data = {
    "passwd": YOUR_HASH_PASSWD,
    "values": {
        "date": "2025-03-13",
        "time": "16:30:00",
        "indoor_temp": 23,
        "indoor_humidity": 67
    }
}

response = requests.post("http://127.0.0.1:8080/send-to-bigquery", json=data)
print(response.status_code, response.text)
