"""
Script to scrape Bitcoin price data from Yahoo Finance for specified dates using playwright api.
"""


# Import necessary libraries
import os
import time
import pandas as pd
from playwright.sync_api import sync_playwright
from datetime import datetime, timezone
from pathlib import Path


def find_project_root(marker=".gitignore"):
    """
    Find the project root directory by looking for a specific marker file.
    """
    path = Path(__file__).resolve()
    for parent in path.parents:
        if (parent / marker).exists():
            return parent
    raise FileNotFoundError(f"Project root not found with marker: {marker}")


def main():
    """
    Scrapes data from Yahoo Finance using playwright api
    """
    with sync_playwright() as p:
        # Launch browser (headless=False lets you see it happen)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Converting period to utc for url
        start_date = "2018-01-01"
        end_date = "2026-01-01"
        period1 = int(datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())
        period2 = int(datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())
        url = f"https://finance.yahoo.com/quote/BTC-EUR/history/?period1={period1}&period2={period2}"

        print("Navigating to Yahoo Finance...")
        page.goto(url, timeout=60000)

        # Accept cookies
        try:
            # Look for "Accept All" or "Agree" button
            accept_button = page.get_by_role("button", name="Alle akzeptieren")
            if accept_button.is_visible():
                accept_button.click()
                print("Cookie consent accepted.")
        except Exception:
            print("No cookie consent overlay found.")

        # Wait to load table
        page.wait_for_selector('table')
        
        # Scrapping table rows
        print("Scraping table data...")
        
        history_list = []
        
        # Scroll the page so that site loads all data
        for _ in range(20):
            page.mouse.wheel(0, 5000)
            time.sleep(1)

        rows = page.query_selector_all('table tbody tr')
        print(f"Found {len(rows)} rows of data.")

        for row in rows:
            cols = row.query_selector_all('td')
            if len(cols) >= 6:
                # Extracting Date and Close Price
                entry = {
                    'Date': cols[0].inner_text(),
                    'Open': cols[1].inner_text().replace(',', ''),
                    'High': cols[2].inner_text().replace(',', ''),
                    'Low': cols[3].inner_text().replace(',', ''),
                    'Close': cols[4].inner_text().replace(',', ''),
                    'Volume': cols[6].inner_text().replace(',', '')
                }
                history_list.append(entry)

        # Creating data dir if does not exists
        if not os.path.exists('data'):
            os.makedirs('data')

        df = pd.DataFrame(history_list)
        
        # Drop non-numeric rows
        df = df[df['Close'].str.contains(r'\d', na=False)]
        project_root = find_project_root()
        csv_path = project_root / "data/bitcoin_stock_data.csv"
        df.to_csv(csv_path, index=False)
        print(f"Data saved. Total rows: {len(df)}")

        browser.close()

if __name__ == "__main__":
    main()