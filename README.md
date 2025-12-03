# NSE Intraday Momentum Tracker

An automated Python tool for identifying and ranking NSE stocks with positive intraday momentum based on price and volume trends.

## 📊 Overview

This project analyzes live intraday data from the National Stock Exchange (NSE) to identify stocks showing upward momentum during trading sessions. It helps traders capitalize on short-term trading opportunities by ranking stocks based on their momentum score.

## ✨ Features

- 🔄 **Live Data Scraping**: Fetches real-time intraday data from NSE
- 📈 **Trend Identification**: Identifies stocks with positive price and volume trends
- 🎯 **Momentum Scoring**: Calculates momentum score = (Price Change % × Volume Change %)
- 📋 **Smart Ranking**: Ranks stocks by momentum score for easy decision-making
- 💾 **Data Export**: Saves results to JSON for further analysis
- 🛡️ **Fallback Mode**: Uses simulated data if API access fails

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/nse-momentum-tracker.git
cd nse-momentum-tracker
```

2. Install required packages:
```bash
pip install requests
```

### Usage

**Option 1: Run Combined Script (Recommended)**
```bash
python momentum_tracker.py
```

**Option 2: Run Separate Scripts**
```bash
# Step 1: Scrape data
python script1_scraper.py

# Step 2: Analyze momentum
python script2_analysis.py
```

## 📁 Project Structure

```
nse-momentum-tracker/
│
├── momentum_tracker.py          # Combined script (all-in-one)
├── script1_scraper.py          # Data scraping module
├── script2_analysis.py         # Momentum analysis module
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Git ignore file
```

## 🔍 How It Works

### 1. Data Collection
- Scrapes live data for NIFTY 50 stocks from NSE API
- Captures current price and trading volume
- Timestamps each data point

### 2. Trend Detection
- Compares current values (10:30 AM) with market open (9:30 AM)
- Identifies stocks where **both** price AND volume increased
- Filters out stocks showing negative or mixed trends

### 3. Momentum Calculation
```
Momentum Score = Price Change % × Volume Change %

Where:
- Price Change % = [(Current Price - Price at 9:30 AM) / Price at 9:30 AM] × 100
- Volume Change % = [(Current Volume - Volume at 9:30 AM) / Volume at 9:30 AM] × 100
```

### 4. Ranking & Output
- Ranks stocks by momentum score (highest first)
- Displays detailed analysis of top performers
- Exports results to JSON

## 📊 Sample Output

```
==========================================
       MOMENTUM RANKINGS
==========================================
Rank   Symbol         Price Chg %   Volume Chg %   Momentum Score
1      RELIANCE       +2.15%        +125.50%       269.83
2      TCS            +1.85%        +98.20%        181.67
3      HDFCBANK       +1.45%        +110.35%       160.01
...
```

## 🎯 Use Cases

- **Day Trading**: Identify high-momentum stocks for intraday positions
- **Market Analysis**: Understand which sectors are gaining momentum
- **Research**: Backtest momentum strategies with historical data
- **Learning**: Educational tool for understanding market dynamics

## ⚙️ Configuration

You can customize the stock list in the script:

```python
nifty50_symbols = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK',
    # Add more symbols here
]
```

## 📝 Requirements

- Python 3.7+
- requests library

See `requirements.txt` for complete dependencies.

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**. 

- Not financial advice
- Past performance doesn't guarantee future results
- Always do your own research before trading
- The author is not responsible for any trading losses

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

## 📜 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- NSE India for providing market data
- Python community for excellent libraries

---

**Made with ❤️ for traders and developers**
