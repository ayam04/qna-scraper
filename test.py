from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

ib_url = "https://www.interviewbit.com/technical-interview-questions/"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--diable-cookies")

driver = webdriver.Chrome()

roles = {}

def get_ib_roles():
    print('Getting interviewbit Roles..')
    
    driver.get(ib_url)
    try:
        wait = WebDriverWait(driver, 10)
        programming_language_div = wait.until(EC.presence_of_element_located((By.ID, "programming-language-tools-technologies")))
    except Exception as e:
        print(e)    
    else:
        anchor_tags = programming_language_div.find_elements(By.TAG_NAME, "a")

    for anchor in anchor_tags:
        roles[anchor.text.replace("Interview","").strip()] = anchor.get_attribute("href")
    
    with open('roles.json', 'w', encoding="utf-8") as f:
        json.dump(roles, f, indent=4)

def ask_role():
    pass

get_ib_roles()

driver.quit()
