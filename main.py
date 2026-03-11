from tinydb import TinyDB
from flask import Flask, render_template, request
import requests

app = Flask(__name__)
db = TinyDB('usrs.json')


@app.route("/")
def index():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr
    if ip == "127.0.0.1":
        ip = ""

    db.insert({'ip': ip})
    print("IP:", ip)

    lat, lon, country = getCoords(ip)

    if not lat:
        return "Unknown location"

    weather = getWeather(lat, lon)

    return render_template("index.html", weather=weather, country=country)


def getCoords(ip):
    req = requests.get(f"http://ip-api.com/json/{ip}").json()

    if req.get("status") != "success":
        print("IP API failed:", req)
        return None, None

    return req.get("lat"), req.get("lon"), req.get("country")


def getWeather(lat, lon):
    req = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=weathercode"
    ).json()

    code = req["current"]["weathercode"]

    weather_map = {
        0: "Clear sky ☀️",
        1: "Mainly clear 🌤",
        2: "Partly cloudy ⛅",
        3: "Overcast ☁️",
        45: "Fog 🌫",
        48: "Depositing rime fog 🌫",
        51: "Light drizzle 🌦",
        53: "Moderate drizzle 🌦",
        55: "Dense drizzle 🌧",
        61: "Slight rain 🌧",
        63: "Moderate rain 🌧",
        65: "Heavy rain 🌧",
        71: "Slight snow ❄️",
        73: "Moderate snow ❄️",
        75: "Heavy snow ❄️",
        80: "Rain showers 🌦",
        81: "Moderate rain showers 🌦",
        82: "Violent rain showers ⛈",
        95: "Thunderstorm ⛈",
        96: "Thunderstorm with hail ⛈",
        99: "Heavy thunderstorm with hail ⛈",
    }

    return weather_map.get(code, "Unknown")


if __name__ == "__main__":
    app.run(debug=True)