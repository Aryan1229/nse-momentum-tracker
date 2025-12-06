from flask import Flask, jsonify, render_template, send_file
from flask_cors import CORS
import yfinance as yf
import pandas as pd
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

stock_data_cache = []
momentum_results_cache = []

NIFTY50_SYMBOLS = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
    'HINDUNILVR.NS', 'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'BAJFINANCE.NS',
    'KOTAKBANK.NS', 'LT.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS',
    'SUNPHARMA.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'NESTLEIND.NS', 'WIPRO.NS'
]


def fetch_intraday_data_yfinance():
    """
    Fetch ACTUAL intraday data using yFinance
    Gets real 9:30 AM and current prices - NO ASSUMPTIONS
    """
    try:
        all_stock_data = []
        today = datetime.now().date()
        
        for symbol in NIFTY50_SYMBOLS[:10]: 
            try:
                display_symbol = symbol.replace('.NS', '')
                
                ticker = yf.Ticker(symbol)
                df = ticker.history(
                    period='1d',
                    interval='1m',
                    start=today,
                    prepost=False
                )
                
                if df.empty:
                    continue
                
                market_open_time = pd.Timestamp(f"{today} 09:30:00", tz=df.index.tz)
                time_930 = df.index[df.index >= market_open_time].min()
                
                if pd.isna(time_930):
                    continue
                
                data_930 = df.loc[time_930]
                price_930 = float(data_930['Close'])
                volume_930 = int(data_930['Volume'])
                
                current_time = df.index.max()
                data_current = df.loc[current_time]
                current_price = float(data_current['Close'])
                current_volume = int(df['Volume'].sum())
                
                all_stock_data.append({
                    'symbol': display_symbol,
                    'price_930': price_930,
                    'volume_930': volume_930,
                    'current_price': current_price,
                    'current_volume': current_volume,
                    'current_time': current_time.strftime('%H:%M:%S'),
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"Error fetching {symbol}: {e}")
                continue
        
        return all_stock_data
    
    except Exception as e:
        print(f"Error in fetch_intraday_data_yfinance: {e}")
        return []


def calculate_momentum(stock_data):
    """
    Calculate momentum using ACTUAL prices - NO ASSUMPTIONS
    """
    results = []
    
    for stock in stock_data:
        price_930 = stock['price_930']
        current_price = stock['current_price']
        volume_930 = stock['volume_930']
        current_volume = stock['current_volume']
        
        price_change = current_price - price_930
        price_change_pct = (price_change / price_930) * 100
        
        volume_change = current_volume - volume_930
        volume_change_pct = (volume_change / volume_930) * 100 if volume_930 > 0 else 0
        
        if price_change > 0 and volume_change > 0:
            momentum_score = price_change_pct * volume_change_pct
            
            results.append({
                'symbol': stock['symbol'],
                'price_930': price_930,
                'current_price': current_price,
                'price_change_pct': round(price_change_pct, 2),
                'volume_930': volume_930,
                'current_volume': current_volume,
                'volume_change_pct': round(volume_change_pct, 2),
                'momentum_score': round(momentum_score, 2),
                'current_time': stock['current_time']
            })
    
    results.sort(key=lambda x: x['momentum_score'], reverse=True)
    return results


@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')


@app.route('/api/fetch-data', methods=['GET'])
def fetch_data():
    """
    API endpoint to fetch live stock data using yFinance
    Uses ACTUAL intraday prices - no assumptions
    """
    global stock_data_cache
    
    try:
        stock_data_cache = fetch_intraday_data_yfinance()
        
        if not stock_data_cache:
            return jsonify({
                'success': False,
                'message': 'No data available. Market might be closed or data fetch failed.',
                'count': 0
            }), 400
        
        return jsonify({
            'success': True,
            'data': stock_data_cache,
            'count': len(stock_data_cache),
            'timestamp': datetime.now().isoformat(),
            'message': f'Fetched ACTUAL intraday data for {len(stock_data_cache)} stocks',
            'source': 'yFinance (Real 9:30 AM prices)'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to fetch data'
        }), 500


@app.route('/api/analyze', methods=['GET'])
def analyze():
    """
    API endpoint to analyze momentum
    Uses ACTUAL prices - NO ASSUMPTIONS
    """
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
            'message': f'Found {len(momentum_results_cache)} trending stocks',
            'note': 'Using ACTUAL 9:30 AM prices - NO assumptions made'
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
        'last_update': datetime.now().isoformat(),
        'data_source': 'yFinance API',
        'method': 'ACTUAL intraday prices (no assumptions)'
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
        'version': '2.0.0',
        'data_source': 'yFinance API',
        'method': 'ACTUAL intraday prices'
    })


if __name__ == '__main__':
    print("=" * 80)
    print("🚀 NSE Momentum Tracker - Server Starting...")
    print("=" * 80)
    print("📊 Dashboard URL: http://localhost:5000")
    print("🔌 Data Source: yFinance API")
    print("✅ Method: ACTUAL 9:30 AM prices (NO assumptions)")
    print("=" * 80)
    print("🔌 API Endpoints:")
    print("   - GET  /api/fetch-data          Fetch ACTUAL intraday data")
    print("   - GET  /api/analyze             Analyze momentum (no assumptions)")
    print("   - GET  /api/stats               Get statistics")
    print("   - GET  /api/export              Export results")
    print("   - GET  /api/top-performers/N    Get top N stocks")
    print("   - GET  /api/stock/<symbol>      Get stock details")
    print("   - GET  /api/health              Health check")
    print("=" * 80)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
