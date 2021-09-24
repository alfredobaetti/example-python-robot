from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
import time
import os


class Challenge:

    agencies_info = {}
    uii_links = []
    columns_names = []
    ind_inv_table = {}

    def __init__(self, url):
        self.driver = Selenium()
        self.excel = Files()

        self.driver.set_download_directory(os.path.join(os.getcwd(), f"output/"))
        self.driver.open_available_browser(url)
        self.driver.maximize_browser_window()

    def click_dive_in(self):
        self.driver.wait_until_page_contains('DIVE IN')
        self.driver.find_element('//a[@class="btn btn-default btn-lg-2x trend_sans_oneregular"]').click()

    def scrape_agencies_amounts(self):
        time.sleep(5)
        AGENCIES = []
        AMOUNTS = []
        while True:
            try:
                agencies = self.driver.find_elements('//div[@id="agency-tiles-widget"]//span[@class="h4 w200"]')
                amounts = self.driver.find_elements('//div[@id="agency-tiles-widget"]//span[@class=" h1 w900"]')
                break
            except:
                pass

        for i in range(len(agencies)):
            AGENCIES.append(agencies[i].text)
            AMOUNTS.append(amounts[i].text)

        self.agencies_info = {'Agencie': AGENCIES, 'Amount': AMOUNTS}
        self.write_amounts_to_excel()

    def write_amounts_to_excel(self):
        file = self.excel.create_workbook(f"output/challenge.xlsx")

        file.append_worksheet("Sheet", self.agencies_info)
        file.rename_worksheet("Agencies", "Sheet")
        file.save()

    def get_columns_names(self):
        self.columns_names = [] # reset just in case
        while True:
            try:        
                columns = self.driver.find_elements("//div[@class='dataTables_scrollHeadInner']//th")
                if columns:   
                    break
            except:
                pass

        for col in columns:
            self.columns_names.append(col.text)

    def scrape_table_agency(self, agency_id):
        try:
            self.driver.find_elements('//*[@id="agency-tiles-widget"]/div/div/div/div/div/div')[agency_id].click()
        except:
            print("Agency was not found")

        while True:
            try:
                self.driver.click_element_when_visible('//select[@name="investments-table-object_length"]')
                self.driver.click_element_when_visible('//*[@id="investments-table-object_length"]/label/select/option[4]')
                break
            except:
                pass

        while True:
            try:
                if self.driver.find_element('investments-table-object_next').get_attribute("class") == 'paginate_button next disabled':
                    self.get_columns_names()
                    for col_name in self.columns_names:
                        self.ind_inv_table[col_name] = []

                    table_trs = self.driver.find_elements('//*[@id="investments-table-object"]/tbody/tr')
                    break
            except:
                pass


        for tr in table_trs:
            for i, td in enumerate(tr.find_elements_by_tag_name("td")):
                try:
                    self.ind_inv_table[self.columns_names[i]].append(td.text)
                except:
                    self.ind_inv_table[self.columns_names[i]].append("")
                    
        self.write_table_to_excel()
    
    def write_table_to_excel(self):
        file = self.excel.open_workbook(f"output/challenge.xlsx")
        file.create_worksheet("Individual Investments")
        file.append_worksheet("Individual Investments", self.ind_inv_table, self.columns_names)
        file.save()

    def get_uii_links(self):
        all_uiis = self.driver.find_elements('//*[@id="investments-table-object"]/tbody/tr/td[1]/a')
        for uii in all_uiis:
            self.uii_links.append(uii.get_attribute("href"))


    def download_UII_pdf(self):
        self.get_uii_links()

        for link in self.uii_links:

            self.driver.go_to(link)

            self.driver.click_element_when_visible('//*[@id="business-case-pdf"]/a')

            while True:
                try:
                    time.sleep(1)
                    if self.driver.find_element('//div[@id="business-case-pdf"]').find_element_by_tag_name("span"):
                        time.sleep(1)
                    else:
                        break
                except:
                    if self.driver.find_element('//*[contains(@id,"business-case-pdf")]//a[@aria-busy="false"]'):
                        time.sleep(1)
                        break


    def close_all_browsers(self):
        self.driver.close_all_browsers()


