# Investing Backtracker

## Motivation
I built Investing Backtracker to get some practice with Flask, using APIs, and displaying data with Chart.js.  
Along the way, I learned how to pull in stock data, set up a basic backend, and make simple interactive charts. It also helped me get a bit more comfortable with handling environment variables and building a basic web app from scratch.

## What It Does
Investing Backtracker lets you:
- Type in a stock ticker.
- See an interactive candlestick chart of the stock's historical data.
- Choose a trading strategy and backtest it on that stock.
- View basic results like total return and number of trades.

It's a simple tool to quickly explore how different strategies would have performed.
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

## Example Pages
<img width="1725" alt="image" src="https://github.com/user-attachments/assets/0fb4be64-a96a-4efd-bade-6111aaf432d0" />

<img width="1725" alt="image" src="https://github.com/user-attachments/assets/c3053aa1-3a02-4cb3-a560-34dd9c0816a0" />



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
