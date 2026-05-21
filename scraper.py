import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

def scrape_bvb_stocks():
    """
    Scrapes stock data from BVB website
    Returns a list of stocks with symbol, price, and variation
    """
    try:
        url = "https://bvb.ro/FinancialInstruments/Markets/Shares"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        stocks = []
        
        # Find the main table containing stock data
        table = soup.find('table', {'class': 'table'})
        
        if not table:
            print("Could not find stock table")
            return []
        
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            try:
                cells = row.find_all('td')
                if len(cells) < 4:
                    continue
                
                # Extract data from cells
                symbol = cells[0].get_text(strip=True)
                price = cells[1].get_text(strip=True)
                change = cells[2].get_text(strip=True)
                variation = cells[3].get_text(strip=True)
                
                # Clean up the data
                symbol = symbol.strip()
                price = price.replace(',', '.')
                change = change.replace(',', '.')
                variation = variation.replace(',', '.').replace('%', '')
                
                stocks.append({
                    'symbol': symbol,
                    'price': price,
                    'change': change,
                    'variation': variation
                })
            except Exception as e:
                print(f"Error parsing row: {e}")
                continue
        
        return stocks
    
    except Exception as e:
        print(f"Error scraping BVB website: {e}")
        return []


def save_stocks_to_file(stocks, filename='stocks.json'):
    """
    Saves stock data to a JSON file
    """
    data = {
        'timestamp': datetime.now().isoformat(),
        'stocks': stocks
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Stocks saved to {filename}")


if __name__ == '__main__':
    print("Starting BVB stock scraper...")
    
    # Scrape once
    stocks = scrape_bvb_stocks()
    
    if stocks:
        print(f"Successfully scraped {len(stocks)} stocks")
        save_stocks_to_file(stocks)
    else:
        print("No stocks found or error occurred")
