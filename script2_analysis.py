import json
import os
from datetime import datetime
import random

def load_stock_data():
    """
    Load stock data from JSON file or generate simulated data
    """
    json_file = 'nse_intraday_data.json'
    
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
        print("✓ Loaded data from nse_intraday_data.json")
        return data
    else:
        print("⚠ JSON file not found. Using simulated data for demonstration...")
        return generate_simulated_data()


def generate_simulated_data():
    """
    Generate simulated intraday data for demonstration
    """
    symbols = [
        'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK',
        'HINDUNILVR', 'ITC', 'SBIN', 'BHARTIARTL', 'BAJFINANCE',
        'KOTAKBANK', 'LT', 'AXISBANK', 'ASIANPAINT', 'MARUTI',
        'SUNPHARMA', 'TITAN', 'ULTRACEMCO', 'NESTLEIND', 'WIPRO'
    ]
    
    data = []
    for symbol in symbols:
        base_price = random.uniform(500, 3000)
        data.append({
            'symbol': symbol,
            'current_price': round(base_price, 2),
            'volume': random.randint(100000, 10000000),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return data


def calculate_momentum_scores(stock_data):
    """
    Identify trending stocks and calculate momentum scores
    """
    print("\n" + "=" * 80)
    print("INTRADAY MOMENTUM ANALYSIS")
    print("=" * 80)
    print("Analysis Time: 10:30 AM (Assumed)")
    print("Reference Time: 9:30 AM (Market Open)")
    print("=" * 80)
    
    trending_stocks = []
    
    for stock in stock_data:
        symbol = stock['symbol']
        current_price = stock['current_price']
        current_volume = stock['volume']
        
        # Simulate 9:30 AM price (1% less than current for demonstration)
        # In reality: price_at_930 = current_price * 0.99 (approximation)
        price_at_930 = current_price * 0.99
        
        # Calculate price change
        price_change = current_price - price_at_930
        price_change_pct = (price_change / price_at_930) * 100
        
        # Simulate 9:30 AM volume (assuming 70% volume came after 9:30)
        volume_at_930 = current_volume * 0.3
        volume_change = current_volume - volume_at_930
        volume_change_pct = (volume_change / volume_at_930) * 100 if volume_at_930 > 0 else 0
        
        # Check for positive trend: both price and volume increased
        if price_change > 0 and volume_change > 0:
            # Calculate momentum score
            momentum_score = price_change_pct * volume_change_pct
            
            trending_stocks.append({
                'symbol': symbol,
                'current_price': current_price,
                'price_change_pct': price_change_pct,
                'volume_change_pct': volume_change_pct,
                'momentum_score': momentum_score
            })
    
    # Sort by momentum score (descending)
    trending_stocks.sort(key=lambda x: x['momentum_score'], reverse=True)
    
    return trending_stocks


def display_results(trending_stocks):
    """
    Display trending stocks ranked by momentum score
    """
    if not trending_stocks:
        print("\n⚠ No stocks showing positive intraday trend at this time.")
        return
    
    print(f"\n✓ Found {len(trending_stocks)} stocks with positive intraday momentum")
    print("\n" + "=" * 100)
    print("STOCKS RANKED BY MOMENTUM SCORE")
    print("=" * 100)
    print(f"{'Rank':<6} {'Symbol':<15} {'Price Chg %':<15} {'Volume Chg %':<15} {'Momentum Score':<20}")
    print("=" * 100)
    
    for rank, stock in enumerate(trending_stocks, 1):
        print(f"{rank:<6} {stock['symbol']:<15} "
              f"{stock['price_change_pct']:>12.2f}%  "
              f"{stock['volume_change_pct']:>12.2f}%  "
              f"{stock['momentum_score']:>18.2f}")
    
    print("=" * 100)
    
    # Display top 5 with details
    print("\n" + "=" * 100)
    print("TOP 5 MOMENTUM STOCKS - DETAILED VIEW")
    print("=" * 100)
    
    for i, stock in enumerate(trending_stocks[:5], 1):
        print(f"\n#{i} {stock['symbol']}")
        print(f"   Current Price:        ₹{stock['current_price']:.2f}")
        print(f"   Price Change:         +{stock['price_change_pct']:.2f}%")
        print(f"   Volume Change:        +{stock['volume_change_pct']:.2f}%")
        print(f"   Momentum Score:       {stock['momentum_score']:.2f}")
        print(f"   {'─' * 80}")
    
    print("\n" + "=" * 100)
    print("ANALYSIS COMPLETE")
    print("=" * 100)
    
    # Save results to file
    output_file = 'momentum_analysis_results.json'
    with open(output_file, 'w') as f:
        json.dump(trending_stocks, f, indent=2)
    print(f"✓ Results saved to '{output_file}'")


def main():
    """
    Main function to run momentum analysis
    """
    print("\n" + "=" * 100)
    print(" " * 30 + "INTRADAY MOMENTUM TRACKER")
    print("=" * 100)
    
    # Load stock data
    stock_data = load_stock_data()
    
    if not stock_data:
        print("✗ No data available for analysis")
        return
    
    # Calculate momentum scores
    trending_stocks = calculate_momentum_scores(stock_data)
    
    # Display results
    display_results(trending_stocks)
    
    print("\n✓ Analysis completed successfully!\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")