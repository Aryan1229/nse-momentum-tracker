import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import json

NIFTY50_SYMBOLS = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'ICICIBANK.NS',
    'HINDUNILVR.NS', 'ITC.NS', 'SBIN.NS', 'BHARTIARTL.NS', 'BAJFINANCE.NS',
    'KOTAKBANK.NS', 'LT.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'MARUTI.NS',
    'SUNPHARMA.NS', 'TITAN.NS', 'ULTRACEMCO.NS', 'NESTLEIND.NS', 'WIPRO.NS'
]


def fetch_intraday_data():
    """
    Fetch intraday data using yFinance
    Gets actual 9:30 AM and 10:30 AM prices and volumes
    """
    
    print("=" * 80)
    print(" " * 25 + "NSE INTRADAY DATA SCRAPER")
    print(" " * 28 + "Using yFinance API")
    print("=" * 80)
    print(f"Fetching Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Number of Stocks: {len(NIFTY50_SYMBOLS)}")
    print("=" * 80 + "\n")
    
    all_stock_data = []
    
    for symbol in NIFTY50_SYMBOLS:
        try:
            display_symbol = symbol.replace('.NS', '')
            
            ticker = yf.Ticker(symbol)
            
            today = datetime.now().date()
            
            df = ticker.history(
                period='1d',
                interval='1m',
                start=today,
                prepost=False
            )
            
            if df.empty:
                print(f"✗ {display_symbol:15} | No data available")
                continue
            
            market_open_time = pd.Timestamp(f"{today} 09:30:00", tz=df.index.tz)
            
            time_930 = df.index[df.index >= market_open_time].min()
            
            if pd.isna(time_930):
                print(f"✗ {display_symbol:15} | Market not open yet")
                continue
            
            data_930 = df.loc[time_930]
            price_930 = data_930['Close']
            volume_930 = data_930['Volume']
            
            current_time = df.index.max()
            data_current = df.loc[current_time]
            current_price = data_current['Close']
            current_volume = df['Volume'].sum()  
            
            stock_data = {
                'symbol': display_symbol,
                'price_930': float(price_930),
                'volume_930': int(volume_930),
                'current_price': float(current_price),
                'current_volume': int(current_volume),
                'current_time': current_time.strftime('%H:%M:%S'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            all_stock_data.append(stock_data)
            
            print(f"✓ {display_symbol:15} | 9:30 Price: ₹{price_930:10.2f} | "
                  f"Current: ₹{current_price:10.2f} | Volume: {current_volume:,}")
        
        except Exception as e:
            print(f"✗ {display_symbol:15} | Error: {str(e)[:50]}")
            continue
    
    output_file = 'nse_intraday_data.json'
    with open(output_file, 'w') as f:
        json.dump(all_stock_data, f, indent=2)
    
    print("\n" + "=" * 80)
    print(f"✓ Data saved to '{output_file}'")
    print(f"✓ Successfully fetched {len(all_stock_data)} stocks")
    print("=" * 80)
    
    return all_stock_data


if __name__ == "__main__":
    try:
        print("\n🚀 Starting intraday data fetch using yFinance...\n")
        data = fetch_intraday_data()
        
        if data:
            print(f"\n✓ Scraping completed successfully!")
            print(f"✓ {len(data)} stocks processed")
            print(f"✓ Run 'python script2_analysis.py' to analyze momentum")
        else:
            print("\n⚠ No data could be fetched. Market might be closed.")
            
    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")
