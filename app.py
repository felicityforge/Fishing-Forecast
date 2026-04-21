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

    # Placeholder forecast logic
    forecast_score = 75  # Replace with real logic later
    return jsonify({
        "lat": lat,
        "lon": lon,
        "species": species,
        "date": date_str,
        "forecast_score": forecast_score,
        "message": f"Predicted fishing activity for {species} on {date_str} is {forecast_score}%."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
