from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.PDF import PDF
from RPA.Tables import Tables
import time
import os
import re
import pandas as pd
#from constants import DOWNLOAD_DIR, URL


driver = Selenium()
excel = Files()
pdf = PDF()
tables = Tables()

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
    driver.click_element_when_visible('//select[@name="investments-table-object_length"]')
    driver.click_element_when_visible('//*[@id="investments-table-object_length"]/label/select/option[4]')

    time.sleep(10)

    inv_table = driver.find_element('//table[@id="investments-table-object"]')
    
    write_table_to_excel(inv_table)


def write_table_to_excel(table):
    tab_html = table.get_attribute('outerHTML')
    tab_dfs = pd.read_html(tab_html)

    file = excel.open_workbook(f"challenge.xlsx")
    file.create_worksheet("Individual Investments")
    # df = pd.DataFrame(columns=tab_dfs[0].columns)

    # for row in tab_dfs[0].iterrows:    
    #     df.append(row)

    #file.append_worksheet("Individual Investments", tab_dfs[0])

    with pd.ExcelWriter('challenge.xlsx', mode='a') as writer:  
        tab_dfs[0].to_excel(writer, sheet_name='Individual Investments')

    time.sleep(15)

def download_UII_pdf():
    UII = driver.find_elements('//*[@id="investments-table-object"]/tbody/tr/td[1]/a')
    current_page = driver.get_location()
    for i in range(len(UII)):
        #driver.open_chrome_browser(UII[i])
        #link = UII[i].get_attribute("href")
        UII = driver.find_elements('//*[@id="investments-table-object"]/tbody/tr/td[1]/a')
        driver.click_link(UII[i])

        uii_pdf = driver.click_element_when_visible('//*[@id="business-case-pdf"]/a')

        time.sleep(5)

        driver.go_to(current_page)

        time.sleep(10)




def main():
    url = 'https://itdashboard.gov/'
    try:
        click_dive_in(url)
        scrape_agencies_amounts()
        scrape_table_agency()
        download_UII_pdf()
    finally:
        driver.close_all_browsers()


if __name__ == "__main__":
    main()