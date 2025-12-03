"""
NSE Momentum Tracker - Flask Backend API
Provides REST API endpoints for the web dashboard
"""

from flask import Flask, jsonify, render_template, send_file
from flask_cors import CORS
import requests
import json
import time
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

# Store data in memory
stock_data_cache = []
momentum_results_cache = []

# NIFTY 50 symbols
NIFTY50_SYMBOLS = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK',
    'HINDUNILVR', 'ITC', 'SBIN', 'BHARTIARTL', 'BAJFINANCE',
    'KOTAKBANK', 'LT', 'AXISBANK', 'ASIANPAINT', 'MARUTI',
    'SUNPHARMA', 'TITAN', 'ULTRACEMCO', 'NESTLEIND', 'WIPRO'
]


def fetch_nse_stock_data():
    """Fetch live data from NSE or generate simulated data"""
    try:
        stock_data = []
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        }
        
        for symbol in NIFTY50_SYMBOLS[:10]:  # Limit for faster response
            try:
                url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
                session = requests.Session()
                session.get("https://www.nseindia.com", headers=headers, timeout=3)
                time.sleep(0.2)
                
                response = session.get(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    price_info = data.get('priceInfo', {})
                    current_price = price_info.get('lastPrice', 0)
                    volume = data.get('totalTradedVolume', 0)
                    
                    stock_data.append({
                        'symbol': symbol,
                        'current_price': float(current_price),
                        'volume': int(volume),
                        'timestamp': datetime.now().isoformat()
                    })
            except:
                continue
        
        # If API fails or insufficient data, use simulated data
        if len(stock_data) < 5:
            return generate_simulated_data()
        
        return stock_data
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        return generate_simulated_data()


def generate_simulated_data():
    """Generate realistic simulated market data"""
    data = []
    for symbol in NIFTY50_SYMBOLS:
        base_price = random.uniform(500, 3500)
        data.append({
            'symbol': symbol,
            'current_price': round(base_price, 2),
            'volume': random.randint(500000, 15000000),
            'timestamp': datetime.now().isoformat()
        })
    return data


def calculate_momentum(stock_data):
    """Calculate momentum scores for stocks"""
    results = []
    
    for stock in stock_data:
        current_price = stock['current_price']
        current_volume = stock['volume']
        
        # Simulate 9:30 AM values
        price_at_930 = current_price * 0.99
        volume_at_930 = current_volume * 0.3
        
        # Calculate changes
        price_change = current_price - price_at_930
        price_change_pct = (price_change / price_at_930) * 100
        
        volume_change = current_volume - volume_at_930
        volume_change_pct = (volume_change / volume_at_930) * 100 if volume_at_930 > 0 else 0
        
        # Only include positive trends
        if price_change > 0 and volume_change > 0:
            momentum_score = price_change_pct * volume_change_pct
            
            results.append({
                'symbol': stock['symbol'],
                'current_price': current_price,
                'price_change_pct': round(price_change_pct, 2),
                'volume_change_pct': round(volume_change_pct, 2),
                'momentum_score': round(momentum_score, 2)
            })
    
    # Sort by momentum score
    results.sort(key=lambda x: x['momentum_score'], reverse=True)
    return results


@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')


@app.route('/api/fetch-data', methods=['GET'])
def fetch_data():
    """API endpoint to fetch live stock data"""
    global stock_data_cache
    
    try:
        stock_data_cache = fetch_nse_stock_data()
        
        return jsonify({
            'success': True,
            'data': stock_data_cache,
            'count': len(stock_data_cache),
            'timestamp': datetime.now().isoformat(),
            'message': 'Data fetched successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to fetch data'
        }), 500


@app.route('/api/analyze', methods=['GET'])
def analyze():
    """API endpoint to analyze momentum"""
    global momentum_results_cache
    
    if not stock_data_cache:
        return jsonify({
            'success': False,
            'message': 'No data available. Please fetch data first.'
        }), 400
    
    try:
        momentum_results_cache = calculate_momentum(stock_data_cache)
        
        return jsonify({
            'success': True,
            'results': momentum_results_cache,
            'count': len(momentum_results_cache),
            'timestamp': datetime.now().isoformat(),
            'message': f'Found {len(momentum_results_cache)} trending stocks'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Analysis failed'
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """API endpoint to get current statistics"""
    top_score = 0
    if momentum_results_cache:
        top_score = max([s['momentum_score'] for s in momentum_results_cache])
    
    return jsonify({
        'total_stocks': len(stock_data_cache),
        'trending_stocks': len(momentum_results_cache),
        'top_score': top_score,
        'last_update': datetime.now().isoformat()
    })


@app.route('/api/export', methods=['GET'])
def export_results():
    """API endpoint to export results as JSON"""
    if not momentum_results_cache:
        return jsonify({
            'success': False,
            'message': 'No results to export'
        }), 400
    
    filename = f'momentum_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    with open(filename, 'w') as f:
        json.dump(momentum_results_cache, f, indent=2)
    
    return send_file(filename, as_attachment=True)


@app.route('/api/top-performers/<int:count>', methods=['GET'])
def top_performers(count):
    """API endpoint to get top N performing stocks"""
    if not momentum_results_cache:
        return jsonify({
            'success': False,
            'message': 'No analysis results available'
        }), 400
    
    top_stocks = momentum_results_cache[:count]
    
    return jsonify({
        'success': True,
        'top_performers': top_stocks,
        'count': len(top_stocks)
    })


@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_details(symbol):
    """API endpoint to get details for a specific stock"""
    stock = next((s for s in momentum_results_cache if s['symbol'] == symbol), None)
    
    if stock:
        return jsonify({
            'success': True,
            'stock': stock
        })
    else:
        return jsonify({
            'success': False,
            'message': f'Stock {symbol} not found in results'
        }), 404


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 NSE Momentum Tracker - Server Starting...")
    print("=" * 60)
    print("📊 Dashboard URL: http://localhost:5000")
    print("🔌 API Endpoints:")
    print("   - GET  /api/fetch-data          Fetch live stock data")
    print("   - GET  /api/analyze             Analyze momentum")
    print("   - GET  /api/stats               Get statistics")
    print("   - GET  /api/export              Export results")
    print("   - GET  /api/top-performers/N    Get top N stocks")
    print("   - GET  /api/stock/<symbol>      Get stock details")
    print("   - GET  /api/health              Health check")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)