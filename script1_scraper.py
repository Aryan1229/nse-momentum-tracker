import requests
import json
import time
from datetime import datetime

def fetch_nse_data():
    """
    Fetches live intraday data for NIFTY 50 stocks from NSE
    """
        
    nifty50_symbols = [
        'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK',
        'HINDUNILVR', 'ITC', 'SBIN', 'BHARTIARTL', 'BAJFINANCE',
        'KOTAKBANK', 'LT', 'AXISBANK', 'ASIANPAINT', 'MARUTI',
        'SUNPHARMA', 'TITAN', 'ULTRACEMCO', 'NESTLEIND', 'WIPRO'
    ]
    
    print("=" * 80)
    print("NSE INTRADAY DATA SCRAPER")
    print("=" * 80)
    print(f"Scraping Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Number of Stocks: {len(nifty50_symbols)}")
    print("=" * 80)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    stock_data = []
    
    for symbol in nifty50_symbols:
        try:
            url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
            
            session = requests.Session()
            session.get("https://www.nseindia.com", headers=headers)
            time.sleep(0.5)  
            
            response = session.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                price_info = data.get('priceInfo', {})
                current_price = price_info.get('lastPrice', 0)
                
                total_traded_volume = data.get('preOpenMarket', {}).get('totalTradedVolume', 0)
                if total_traded_volume == 0:
                    total_traded_volume = data.get('totalTradedVolume', 0)
                
                stock_data.append({
                    'symbol': symbol,
                    'current_price': current_price,
                    'volume': total_traded_volume,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
                print(f"✓ {symbol:15} | Price: ₹{current_price:10.2f} | Volume: {total_traded_volume:15,}")
            
            else:
                print(f"✗ {symbol:15} | Failed to fetch data (Status: {response.status_code})")
        
        except Exception as e:
            print(f"✗ {symbol:15} | Error: {str(e)[:50]}")
        
        time.sleep(0.5)  
    
    output_file = 'nse_intraday_data.json'
    with open(output_file, 'w') as f:
        json.dump(stock_data, f, indent=2)
    
    print("=" * 80)
    print(f"✓ Data saved to '{output_file}'")
    print(f"✓ Successfully scraped {len(stock_data)} stocks")
    print("=" * 80)
    
    return stock_data


if __name__ == "__main__":
    try:
        data = fetch_nse_data()
        print(f"\n✓ Scraping completed successfully!")
        print(f"✓ Run 'python script2_analysis.py' to analyze the data")
    except Exception as e:
        print(f"\n✗ Error occurred: {str(e)}")

        print("\nNote: If NSE API fails, the script will use simulated data in Script 2")
