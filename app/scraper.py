import cloudscraper
from bs4 import BeautifulSoup

def fetch_mcb_data(url, start_date, end_date, cat):

    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "windows",
            "mobile": False
        }
    )

    # open page where form exists (IMPORTANT)
    scraper.get(url)

    payload = {
        "a[from]": start_date,
        "a[to]": end_date,
        "a[cat]": cat,
        "btn_submit": "Submit"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": url,
        "Origin": "https://www.mcbfunds.com",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = scraper.post(url, data=payload, headers=headers)

    print(response.status_code)

    soup = BeautifulSoup(response.text, "lxml")
    table = soup.find("table", {"id": "table2"})

    data = []

    if table:
        headers = [th.text.strip() for th in table.find_all("th")]

        for row in table.find_all("tr")[1:]:
            cols = [td.text.strip() for td in row.find_all("td")]
            if cols:
                data.append(dict(zip(headers, cols)))

    return data
