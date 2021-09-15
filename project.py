## automating web browser interaction
from matplotlib.pyplot import table
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By 
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select

# data management and time
import pandas as pd
import numpy as np
import time

driver = webdriver.Chrome(ChromeDriverManager().install())
url = 'https://itdashboard.gov/'

def scrape_agencies_amounts():
    driver.get(url)
    driver.maximize_window()
    
    delay = 10

    """Find and click in DIVE IN"""
    element_present = EC.presence_of_element_located((By.ID, 'block-nodeblock-top-buttons'))
    WebDriverWait(driver, delay).until(element_present)

    element1 = driver.find_element_by_id("block-nodeblock-top-buttons")
    ActionChains(driver).click(element1).perform()

    """Find agencies and amounts. Append to two lists"""
    AGENCIES = []
    AMOUNTS = []

    element_present = EC.presence_of_all_elements_located((By.XPATH, '/html/body/main/div[1]/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div/div[1]/a/span[1]'))
    WebDriverWait(driver, delay).until(element_present)
    agencies = driver.find_elements_by_xpath("/html/body/main/div[1]/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div/div[1]/a/span[1]")

    element_present = EC.presence_of_all_elements_located((By.XPATH, '/html/body/main/div[1]/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div/div[1]/a/span[2]'))
    WebDriverWait(driver, delay).until(element_present)
    amounts = driver.find_elements_by_xpath("/html/body/main/div[1]/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div/div[1]/a/span[2]")
    
    for c in range(len(agencies)):
        AGENCIES.append(agencies[c].text)
        AMOUNTS.append(amounts[c].text)
    
    write_amounts_to_excel(AGENCIES, AMOUNTS)



def write_amounts_to_excel(ag, am):
    
    """Create Dataframe from lists and write it in an excel file"""
    df = pd.DataFrame(list(zip(ag, am)),
                   columns =['Agencies', 'Amounts'])
    
    df.to_excel('challenge.xlsx',sheet_name='Agencies')


def scrape_table_agency():

    """Find agency and go to its page"""
    delay = 10

    element_present = EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[1]/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div[9]/div[1]/div/div/div/div[2]/a'))
    WebDriverWait(driver, delay).until(element_present)

    element1 = driver.find_element_by_xpath("/html/body/main/div[1]/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div[9]/div[1]/div/div/div/div[2]/a")
    ActionChains(driver).click(element1).perform()

    """Select to show all entries in the table"""
    delay = 20

    element_present = EC.element_to_be_clickable((By.XPATH, '/html/body/main/div/div/div/div[4]/div/div/div/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div/label/select'))
    WebDriverWait(driver, delay).until(element_present)

    entries = driver.find_element_by_xpath("/html/body/main/div/div/div/div[4]/div/div/div/div[2]/div/div[1]/div/div/div/div/div[2]/div[2]/div/label/select")    
    select = Select(entries)    
    select.select_by_index(3) 

    time.sleep(10)

    """Find table by ID"""
    element_present = EC.presence_of_element_located((By.ID, 'investments-table-object'))
    WebDriverWait(driver, delay).until(element_present)

    inv_table=driver.find_element_by_id('investments-table-object')

    write_table_to_excel(inv_table)


def write_table_to_excel(tab):

    """Create Dataframe from HTML and write table in another sheet of excel file"""
    tab_html=tab.get_attribute('outerHTML')

    tab_dfs=pd.read_html(tab_html)

    with pd.ExcelWriter('challenge.xlsx', mode='a') as writer:  
        tab_dfs[0].to_excel(writer, sheet_name='Individual Investments')


def download_UII_pdf():

    """Find all UIIs which contain links"""
    delay = 20

    element_present = EC.presence_of_all_elements_located((By.XPATH, '/html/body/main/div/div/div/div[4]/div/div/div/div[2]/div/div[1]/div/div/div/div/div[3]/div[2]/table/tbody/tr/td[1]/a'))
    WebDriverWait(driver, delay).until(element_present)

    UII = driver.find_elements_by_xpath("/html/body/main/div/div/div/div[4]/div/div/div/div[2]/div/div[1]/div/div/div/div/div[3]/div[2]/table/tbody/tr/td[1]/a")    
    currenturl=driver.current_url

    """Open UII's links and download PDF"""
    for x in range(len(UII)):

        element_present = EC.presence_of_all_elements_located((By.XPATH, '/html/body/main/div/div/div/div[4]/div/div/div/div[2]/div/div[1]/div/div/div/div/div[3]/div[2]/table/tbody/tr/td[1]/a'))
        WebDriverWait(driver, delay).until(element_present)

        UII = driver.find_elements_by_xpath("/html/body/main/div/div/div/div[4]/div/div/div/div[2]/div/div[1]/div/div/div/div/div[3]/div[2]/table/tbody/tr/td[1]/a")
        UII[x].click()

        element_present = EC.element_to_be_clickable((By.XPATH, '/html/body/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div[6]/a'))
        WebDriverWait(driver, delay).until(element_present)

        PDF = driver.find_element_by_xpath("/html/body/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div[6]/a")
        PDF.click()

        time.sleep(5)

        driver.get(currenturl)

        time.sleep(3)


def main():
    try:
        scrape_agencies_amounts()
        scrape_table_agency()
        download_UII_pdf()

    finally:
        driver.quit()


if __name__ == "__main__":
    main()