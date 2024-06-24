import os
import json
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver_path = "C:/Users/ayamu/python programs/drivers/chromedriver-win64/chromedriver.exe"

ib_url = "https://www.interviewbit.com/technical-interview-questions/"
jtp_url = "https://www.javatpoint.com/interview-questions-and-answers"
itp_url = "https://intellipaat.com/blog/interview-questions/"

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--disable-cookies")

driver = webdriver.Chrome(service=Service(driver_path), options=options)

roles = {}

# Interviewbit Roles

def get_ib_roles():
    print("Getting IB Roles..")
    
    driver.get(ib_url)
    try:
        wait = WebDriverWait(driver, 10)
        programming_language_div = wait.until(EC.presence_of_element_located((By.ID, "programming-language-tools-technologies")))
        anchor_tags = programming_language_div.find_elements(By.TAG_NAME, "a")
    except Exception as e:
        print(e)
        driver.quit()
        return

    for anchor in anchor_tags:
        roles[anchor.text.replace("Interview", "").strip()] = anchor.get_attribute("href")

    for i in roles.values():
        extract_ib_roles(i)

    driver.quit()

def extract_ib_roles(website):
    filename = website.replace("https://www.interviewbit.com/", "").replace("-questions/", "").replace("-interview", "").replace("-questions", "").replace("experience/", "experience")
    try:
        driver.get(website)
        sections = driver.find_elements(By.CLASS_NAME, "ibpage-article-header")
        extracted_data = []
        for section in sections:
            question = section.find_element(By.TAG_NAME, "h3").text.strip()
            answer_elements = section.find_element(By.CLASS_NAME, "ibpage-article")
            answer_text = [element.text.strip() for element in answer_elements.find_elements(By.XPATH, ".//*")]
            answer = " ".join(a.strip() for a in answer_text)

            extracted_data.append({
                "question": question.strip(),
                "answer": answer,
                "reference": "interviewbit.com"
            })
        try:
            os.makedirs("Outputs/Interviewbit", exist_ok=True)
            with open(f"Outputs/Interviewbit/{filename}.json", "x", encoding="utf-8") as f:
                json.dump(extracted_data, f, indent=4)
        except FileExistsError:
            with open(f"Outputs/Interviewbit/{filename}.json", "w", encoding="utf-8") as f:
                json.dump(extracted_data, f, indent=4)
    except Exception as e:
        pass

# Javatpoint Roles

def get_jtp_roles():
    links = []
    print("Getting Javatpoint Roles..")

    driver.get(jtp_url)
    try:
        wait = WebDriverWait(driver, 2)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.leftmenu:nth-of-type(n+6) a")))
        elements = driver.find_elements(By.CSS_SELECTOR, 'div.leftmenu:nth-of-type(n+6) a')
        for element in elements:
            links.append(element.get_attribute('href'))
    except Exception as e:
        print(e)
        driver.quit()
        return
    
    for link in links:
        extract_jtp_roles(link)

    driver.quit()

def extract_jtp_roles(link):
    filename = link.replace("https://www.javatpoint.com/", "").replace("-interview-questions-and-answers", "").replace("-interview-questions", "")
    try:
        driver.get(link)

        h3_elements = driver.find_elements(By.TAG_NAME, 'h3')

        extracted_data = []
        for h3 in h3_elements:
            question = h3.text.split(".")[-1]
            answer = []
            sibling = h3.find_element(By.XPATH, 'following-sibling::*[1]')
            try:
                while sibling.tag_name != 'hr':
                    answer.append(sibling.text)
                    sibling = sibling.find_element(By.XPATH, 'following-sibling::*[1]')
                answer_text = "\n".join(answer).replace("Ans:", "").strip()
            except Exception as e:
                break
            
            extracted_data.append({
                "question": question.strip(),
                "answer": answer_text,
                "reference": "javatpoint.com"
            })
        print(extracted_data)
        try:
            os.makedirs("Outputs/Javatpoint", exist_ok=True)
            with open(f"Outputs/Javatpoint/{filename}.json", "x", encoding="utf-8") as f:
                json.dump(extracted_data, f, indent=4)
        except FileExistsError:
            with open(f"Outputs/Javatpoint/{filename}.json", "w", encoding="utf-8") as f:
                json.dump(extracted_data, f, indent=4)
    except Exception as e:
        pass

# Intellipat Roles

def get_itp_roles():
    print("Getting Intellipat Roles..")
    links = []
    driver.get(itp_url)
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".category-question-list a")))
        elements = driver.find_elements(By.CSS_SELECTOR, ".category-question-list a")
        for element in elements:
            links.append(element.get_attribute('href'))
        # print(len(links))
    except Exception as e:
        print(e)
        driver.quit()
        return

    for link in links:
        extract_itp_roles(link)

    driver.quit()

def extract_itp_roles(link):
    filename = link.replace("https://intellipaat.com/blog/interview-question/", "").replace("-interview-questions/", "")
    try:
        driver.get(link)

        h3_elements = driver.find_elements(By.TAG_NAME, 'h3')

        extracted_data = []
        for h3 in h3_elements:
            question = h3.text
            answer = []
            sibling = h3.find_element(By.XPATH, 'following-sibling::*[1]')
            try:
                while sibling.tag_name != 'h3':
                    answer.append(sibling.text)
                    sibling = sibling.find_element(By.XPATH, 'following-sibling::*[1]')
                answer_text = "\n".join(answer).replace("Ans:", "").strip()
                # print(question, answer_text)
            except Exception as e:
                break
            
            extracted_data.append({
                "question": question.strip(),
                "answer": answer_text,
                "reference": "intellipaat.com"
            })
        print(extracted_data)
        try:
            os.makedirs("Outputs/Intellipaat", exist_ok=True)
            with open(f"Outputs/Intellipaat/{filename}.json", "x", encoding="utf-8") as f:
                json.dump(extracted_data, f, indent=4)
        except FileExistsError:
            with open(f"Outputs/Intellipaat/{filename}.json", "w", encoding="utf-8") as f:
                json.dump(extracted_data, f, indent=4)
    except Exception as e:
        print(e)

# get_ib_roles()
# get_jtp_roles()
get_itp_roles()
# extract_itp_roles("https://intellipaat.com/blog/interview-question/rest-api-interview-questions/")