from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forecast', methods=['GET'])
def forecast():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    species = request.args.get('species')
    date_str = request.args.get('date')

    # Validate date input
    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.today()
        if selected_date < today or selected_date > today + timedelta(days=14):
            return jsonify({"error": "Date must be within 14 days from today."})
    except Exception:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."})

    import random

def generate_forecast(species, date):
    hours = [
        {"block": "06:00–09:00", "activity": random.randint(60, 90)},
        {"block": "09:00–12:00", "activity": random.randint(40, 80)},
        {"block": "12:00–15:00", "activity": random.randint(30, 70)},
        {"block": "15:00–18:00", "activity": random.randint(50, 85)},
        {"block": "18:00–21:00", "activity": random.randint(70, 95)},
    ]
    best_block = max(hours, key=lambda h: h["activity"])
    return {
        "species": species,
        "date": date,
        "best_block": best_block["block"],
        "activity": best_block["activity"],
        "hourly_forecast": hours
    }

@app.route('/forecast', methods=['GET'])
def forecast():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    species = request.args.get('species')
    date_str = request.args.get('date')

    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."})

    report = generate_forecast(species, date_str)
    return jsonify({
        "lat": lat,
        "lon": lon,
        "species": report["species"],
        "date": report["date"],
        "best_hours": report["best_block"],
        "activity_score": report["activity"],
        "hourly_forecast": report["hourly_forecast"],
        "message": f"Best fishing hours for {species} on {date_str} are {report['best_block']} with activity {report['activity']}%."
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
