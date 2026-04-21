from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# ---------- Forecast Logic ----------
def generate_forecast(species, date):
    """Generate a realistic fishing forecast for a single day."""
    # Example hourly forecast blocks
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

# ---------- Routes ----------
@app.route('/')
def index():
    """Render the main form page."""
    return render_template('index.html')

@app.route('/forecast', methods=['GET'])
def forecast():
    """Generate forecasts for a date range."""
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    species = request.args.get('species')
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')

    # Validate date format
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except Exception:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."})

    # Validate range
    if end_date < start_date:
        return jsonify({"error": "End date must be after start date."})

    # Generate daily reports
    reports = []
    current_date = start_date
    while current_date <= end_date:
        report = generate_forecast(species, current_date.strftime("%Y-%m-%d"))
        reports.append(report)
        current_date += timedelta(days=1)

    # Return structured JSON
    return jsonify({
        "lat": lat,
        "lon": lon,
        "species": species,
        "start_date": start_date_str,
        "end_date": end_date_str,
        "reports": reports,
        "message": f"Forecast for {species} from {start_date_str} to {end_date_str} generated successfully."
    })

# ---------- Run ----------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
