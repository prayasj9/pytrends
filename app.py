from flask import Flask, jsonify, request
from pytrends.request import TrendReq
import pandas as pd
import requests

# Flask app setup
app = Flask(__name__)

# Google Apps Script webhook URL (set your actual one here)
APPS_SCRIPT_WEBHOOK = 'https://script.google.com/macros/s/AKfycbwIlAHfnw-zMO1KGjbKuM5OQccQsXtVXmS89SFk1IPO6xhCXT_8Ki7qZmiVmZVlQ/exec'

@app.route("/run-pytrends", methods=["GET"])
def run_pytrends():
    try:
        # Run pytrends
        pytrends = TrendReq()
        pytrends.build_payload(['sunscreen'], timeframe='today 12-m')
        df = pytrends.interest_over_time().reset_index()

        # Convert datetime to string to make it JSON serializable
        for col in df.select_dtypes(include=['datetime64[ns]']).columns:
            df[col] = df[col].astype(str)

        payload = {
            'headers': df.columns.tolist(),
            'rows': df.values.tolist()
        }

        # Send data to Google Apps Script
        res = requests.post(APPS_SCRIPT_WEBHOOK, json=payload)

        return jsonify({'status': 'sent', 'response': res.text})

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/")
def home():
    return "Pytrends API is running on Render!"
