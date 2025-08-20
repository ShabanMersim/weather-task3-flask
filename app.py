import os, random, statistics, requests
from flask import Flask, render_template, jsonify, request

API_KEY = os.getenv("OWM_API_KEY", "YOUR_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
UNITS = "metric"

CITY_POOL = [
    "Sofia,BG","Plovdiv,BG","Varna,BG","Burgas,BG",
    "London,GB","Paris,FR","Berlin,DE","Rome,IT","Madrid,ES",
    "New York,US","Los Angeles,US","Toronto,CA","Vancouver,CA",
    "Tokyo,JP","Seoul,KR","Beijing,CN","Sydney,AU","Melbourne,AU",
    "Cairo,EG","Istanbul,TR","Athens,GR","Stockholm,SE","Oslo,NO",
    "Dubai,AE","Singapore,SG","Bangkok,TH","Rio de Janeiro,BR","Buenos Aires,AR"
]

app = Flask(__name__)

def interpret_condition(d):
    main = d["weather"][0]["main"]
    clouds = d.get("clouds", {}).get("all", 0)
    if main in ("Rain","Drizzle","Thunderstorm"): return "🌧️ Вали"
    if main == "Snow": return "❄️ Сняг"
    if main == "Clear": return "☀️ Слънчево"
    if clouds >= 50: return "☁️ Облачно"
    return f"🌤️ {d['weather'][0]['description'].capitalize()}"

def fetch_weather(city: str):
    try:
        r = requests.get(BASE_URL, params={"q": city, "appid": API_KEY, "units": UNITS}, timeout=10)
        r.raise_for_status()
        d = r.json()
        return {"name": d["name"], "temp": float(d["main"]["temp"]), "humidity": int(d["main"]["humidity"]), "condition": interpret_condition(d)}
    except requests.RequestException as e:
        return {"error": f"{city}: {e}"}

@app.get("/")
def index():
    warn = None if (API_KEY and API_KEY != "YOUR_API_KEY") else "⚠️ Задай OWM_API_KEY преди ползване."
    return render_template("index.html", warning=warn)

@app.get("/api/random")
def api_random():
    cities = random.sample(CITY_POOL, 5)
    items = [x for c in cities if "error" not in (x:=fetch_weather(c))]
    stats = None
    if items:
        coldest = min(items, key=lambda x: x["temp"])
        avg = statistics.mean(x["temp"] for x in items)
        stats = {"coldest_city": coldest["name"], "coldest_temp": coldest["temp"], "avg_temp": avg}
    return jsonify({"items": items, "stats": stats})

@app.get("/api/city")
def api_city():
    q = request.args.get("q", "").strip()
    if not q: return jsonify({"error":"Missing ?q=City,CC"}), 400
    data = fetch_weather(q)
    if "error" in data: return jsonify(data), 400
    return jsonify({"item": data})

if __name__ == "__main__":
    app.run(debug=True)
