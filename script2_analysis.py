import json
import os
from datetime import datetime


def load_stock_data():
    """Load stock data from JSON file"""
    json_file = 'nse_intraday_data.json'
    
    if not os.path.exists(json_file):
        print("✗ Data file not found. Please run script1_scraper.py first.")
        return None
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    print(f"✓ Loaded {len(data)} stocks from {json_file}")
    return data


def calculate_momentum_scores(stock_data):
    """
    Calculate momentum scores using ACTUAL prices
    No assumptions - using real 9:30 AM and current prices
    """
    
    print("\n" + "=" * 80)
    print(" " * 25 + "MOMENTUM ANALYSIS")
    print("=" * 80)
    print("Using ACTUAL 9:30 AM prices from yFinance")
    print("No assumptions - Real intraday data")
    print("=" * 80 + "\n")
    
    trending_stocks = []
    
    for stock in stock_data:
        symbol = stock['symbol']
        
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
            
            trending_stocks.append({
                'symbol': symbol,
                'price_930': price_930,
                'current_price': current_price,
                'price_change_pct': price_change_pct,
                'volume_930': volume_930,
                'current_volume': current_volume,
                'volume_change_pct': volume_change_pct,
                'momentum_score': momentum_score,
                'current_time': stock['current_time']
            })
    
    trending_stocks.sort(key=lambda x: x['momentum_score'], reverse=True)
    
    return trending_stocks


def display_results(trending_stocks):
    """Display momentum analysis results"""
    
    if not trending_stocks:
        print("\n⚠ No stocks showing positive intraday trend at this time.")
        print("This means no stocks have both price AND volume increases since 9:30 AM.")
        return
    
    print(f"\n✓ Found {len(trending_stocks)} stocks with positive momentum")
    
    print("\n" + "=" * 100)
    print(" " * 35 + "MOMENTUM RANKINGS")
    print("=" * 100)
    print(f"{'Rank':<6} {'Symbol':<12} {'9:30 Price':<12} {'Current':<12} "
          f"{'Price Chg':<12} {'Vol Chg':<12} {'Score':<15}")
    print("=" * 100)
    
    for rank, stock in enumerate(trending_stocks, 1):
        print(f"{rank:<6} {stock['symbol']:<12} "
              f"₹{stock['price_930']:>9.2f}  "
              f"₹{stock['current_price']:>9.2f}  "
              f"{stock['price_change_pct']:>9.2f}%  "
              f"{stock['volume_change_pct']:>9.2f}%  "
              f"{stock['momentum_score']:>13.2f}")
    
    print("=" * 100)
    
    print("\n" + "=" * 100)
    print(" " * 32 + "TOP 5 MOMENTUM STOCKS - DETAILED VIEW")
    print("=" * 100)
    
    for i, stock in enumerate(trending_stocks[:5], 1):
        print(f"\n#{i}  {stock['symbol']}")
        print(f"    Time:               {stock['current_time']}")
        print(f"    Price at 9:30 AM:   ₹{stock['price_930']:,.2f}")
        print(f"    Current Price:      ₹{stock['current_price']:,.2f}")
        print(f"    Price Change:       +{stock['price_change_pct']:.2f}%")
        print(f"    Volume at 9:30:     {stock['volume_930']:,}")
        print(f"    Current Volume:     {stock['current_volume']:,}")
        print(f"    Volume Change:      +{stock['volume_change_pct']:.2f}%")
        print(f"    Momentum Score:     {stock['momentum_score']:.2f}")
        print("    " + "─" * 85)
    
    print("\n" + "=" * 100)
    
    output_file = 'momentum_analysis_results.json'
    with open(output_file, 'w') as f:
        json.dump(trending_stocks, f, indent=2)
    
    print(f"✓ Results saved to '{output_file}'")
    print("=" * 100)


def main():
    """Main function"""
    
    print("\n" + "=" * 100)
    print(" " * 30 + "NSE INTRADAY MOMENTUM TRACKER")
    print(" " * 35 + "Real-time Analysis")
    print("=" * 100)
    
    stock_data = load_stock_data()
    
    if not stock_data:
        return
    
    trending_stocks = calculate_momentum_scores(stock_data)
    
    display_results(trending_stocks)
    
    print("\n✓ Analysis completed successfully!")
    print(f"✓ Used ACTUAL intraday prices from yFinance")
    print(f"✓ No assumptions made - Real market data\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
