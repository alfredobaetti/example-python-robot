from itdashboard import Challenge
from agencies import ID

def main():
    challenge = Challenge(url="https://itdashboard.gov/")
    try:
        challenge.click_dive_in()
        challenge.scrape_agencies_amounts()
        challenge.scrape_table_agency(ID)
        challenge.download_UII_pdf()
    finally:
        challenge.close_all_browsers()


if __name__ == "__main__":
    main()