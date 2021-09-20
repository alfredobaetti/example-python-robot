from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.PDF import PDF
import time
import os
import re
#from constants import DOWNLOAD_DIR, URL


driver = Selenium()
excel = Files()
pdf = PDF()

def click_dive_in(url):
    driver.open_chrome_browser(url)
    driver.maximize_browser_window()
    driver.wait_until_page_contains('DIVE IN')
    driver.find_element('//a[@class="btn btn-default btn-lg-2x trend_sans_oneregular"]').click()

def scrape_agencies_amounts():
    time.sleep(5)
    AGENCIES = []
    AMOUNTS = []

    agencies = driver.find_elements('//div[@id="agency-tiles-widget"]//span[@class="h4 w200"]')
    amounts = driver.find_elements('//div[@id="agency-tiles-widget"]//span[@class=" h1 w900"]')

    for i in range(len(agencies)):
        AGENCIES.append(agencies[i].text)
        AMOUNTS.append(amounts[i].text)
    
    agencies_info = {'Agencie': AGENCIES, 'Amount': AMOUNTS}
    write_amounts_to_excel(agencies_info)

def write_amounts_to_excel(info):
    #file = excel.create_workbook(f"{DOWNLOAD_DIR}/{filename}.xlsx")
    file = excel.create_workbook(f"challenge.xlsx")
    
    file.append_worksheet("Sheet", info)
    file.rename_worksheet("Agencies", "Sheet")
    file.save()


def scrape_table_agency():
    element = driver.find_element('//*[@id="agency-tiles-widget"]/div/div[9]/div[1]/div/div/div/div[2]/a')
    element.click()
    driver.wait_until_element_is_visible('//*[@id="investments-table-object_length"]/label/select',timeout=15)
    entries = driver.find_element('//select[@name="investments-table-object_length"]')
    entries.select_from_list_by_index(3) 
    time.time(15)





def main():
    url = 'https://itdashboard.gov/'
    try:
        click_dive_in(url)
        scrape_agencies_amounts()
        scrape_table_agency()
        #download_UII_pdf()
    finally:
        driver.close_all_browsers()


if __name__ == "__main__":
    main()