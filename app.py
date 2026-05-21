from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load stocks from JSON file
def load_stocks():
    """Load stocks from the JSON file created by scraper"""
    try:
        if os.path.exists('stocks.json'):
            with open('stocks.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading stocks: {e}")
    
    return {'timestamp': datetime.now().isoformat(), 'stocks': []}


@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """API endpoint to get all stocks"""
    data = load_stocks()
    return jsonify(data)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    # Run on localhost:5000
    app.run(debug=True, host='0.0.0.0', port=5000)
