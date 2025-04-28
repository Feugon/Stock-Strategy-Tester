# Investing Backtracker

## Project Overview
**Investing Backtracker** is a web app that lets you visualize stock data and backtest trading strategies.  
It shows interactive candlestick charts and strategy results, making it easier to analyze stock performance and explore different trading ideas.

## Technologies Used
- **Flask** — lightweight backend framework.
- **Chart.js** — library for dynamic, interactive charts.
- **chartjs-chart-financial** — extension for candlestick and financial charts.
- **chartjs-adapter-date-fns** — adapter for date handling in Chart.js.
- **chartjs-plugin-annotation** — plugin to add markers and highlights on charts.

## Features
- Display candlestick charts based on historical stock data.
- Backtest trading strategies and view summarized results.
- Simple UI to input stock tickers and select strategies.

## Example Page
<img width="1728" alt="image" src="https://github.com/user-attachments/assets/398929eb-2c44-4976-86f1-62bc5959be1b" />


## Getting Started

### Prerequisites
- Python 3.x
- Flask

### Installation
```bash
git clone <repository-url>
cd InvestingBacktracker
pip install -r requirements.txt
```

### Setting Up Environment Variables
Before running the app, create a `.env` file in the project root and add the following:

```bash
DATABASE_URL=your_database_url_here
STOCK_API_KEY=your_stock_api_key_here
SECRET_KEY=your_secret_key_here
```

- `DATABASE_URL` — the database connection string (e.g., SQLite or PostgreSQL).
- `STOCK_API_KEY` — your API key from the Vantage API (or similar provider).
- `SECRET_KEY` — any random string to keep your Flask sessions secure.

*Note: Your `.env` file is private and should stay out of version control (already handled in `.gitignore`).*

### Running the Application
```bash
flask run
```
Then open your browser and head to `http://localhost:5000`.
