import cloudscraper
from bs4 import BeautifulSoup


def fetch_mcb_data(url, start_date, end_date, cat):
    try:
        scraper = cloudscraper.create_scraper(
            browser={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )

        homepage = "https://www.mcbfunds.com/"
        scraper.get(homepage)

        payload = {
            "a[from]": start_date,
            "a[to]": end_date,
            "a[cat]": cat,
            "btn_submit": "Submit"
        }

        headers = {
            "User-Agent": scraper.headers["User-Agent"],
            "Referer": url,
            "Origin": "https://www.mcbfunds.com",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = scraper.post(url, data=payload, headers=headers)

        if response.status_code != 200:
            return {"error": f"Blocked: {response.status_code}"}

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

    except Exception as e:
        return {"error": str(e)}
