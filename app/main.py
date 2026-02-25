from fastapi import FastAPI
from app.scraper import fetch_mcb_data

app = FastAPI(title="MCB Scraper API")


@app.get("/scrape")
def scrape_data(
    url: str,
    start_date: str,
    end_date: str,
    cat: str
):
    return fetch_mcb_data(url, start_date, end_date, cat)
