#!/usr/bin/env python
# coding: utf-8



from selenium import webdriver
import time 
import pandas as pd
from time import sleep

class h1bgrader_scraper:
    '''
        Scrape data from h1bgrader
        Main purpose is use it to get sponsor comapnies for now.
        @author: Zetan Li
        @version: -1
    '''
    
    
    def __init__(self,chrome_path,website = "https://h1bgrader.com/",sleep_secs = 2):
        '''
            Some init data & parameters
        '''
        self.chrome_path = chrome_path
        self.driver = webdriver.Chrome(self.chrome_path)
        self.website = website
        self.raw_companies = []
        self.sleep_secs = sleep_secs
    def get(self):
        '''
            Open the website through selenium 
        '''
        self.driver.get(self.website)
    def click_search_by_title(self,xpath):
        '''
            Click search by title button
        
        '''
        self.driver.find_element_by_xpath(xpath).click()
    def search_by_title(self,xpath_input,xpath_submit,title = "Data Analyst"):
        '''
            Type in title and click search
        
        '''
        self.driver.find_element_by_xpath(xpath_input).send_keys(title)
        self.driver.find_element_by_xpath(xpath_submit).click()
    def get_maximum_pages(self,pagination_name = "pagination"):
        '''
            Get maximum pages number
        
        '''
        return int(scraper.driver.find_element_by_class_name(pagination_name).find_elements_by_tag_name("li")[-1].text)
    def get_raw_company_list(self,table_id = "h1bsponsor-by-job"):
        '''
            Extract raw company data 
        
        '''
        max_number = self.get_maximum_pages()
        js = "var q=document.documentElement.scrollTop=10000"
        xpath = '//*[@id=' + '"' + table_id + '"' + ']/tbody'
        for i in range(1,max_number+1):            
            self.driver.execute_script(js)
            sleep(self.sleep_secs)
            self.driver.find_element_by_link_text(str(i)).click()
            sleep(self.sleep_secs)
            self.raw_companies.append(self.driver.find_element_by_xpath(xpath).text)
            sleep(self.sleep_secs)
    def get_result_df(self,table_id = "h1bsponsor-by-job"):
        '''
            Process raw company data and return as Pandas DataFrame
        '''
        res2 = []
        self.get_raw_company_list(table_id)
        for i in self.raw_companies:
            res2.extend(i.split('\n'))
        companies = [i.split('(')[0].strip() for i in res2]
        companies = [i.strip() for i in companies]
        case_num = [int(i.split('(')[1].split(')')[0]) for i in res2]
        df = pd.DataFrame({"company":companies,"case_num":case_num})
        return df