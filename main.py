import os
import json
import tkinter as tk
from tkinter import ttk
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ib_url = "https://www.interviewbit.com/technical-interview-questions/"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--diable-cookies")

driver = webdriver.Chrome()

roles = {}

def get_ib_roles():
    print("Getting interviewbit Roles.. \n")
    
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
  with open("roles.json") as f:
    data = json.load(f)

  window = tk.Tk()
  window.title("Select Interview Role")

  def handle_selection(event=None):
    selected_role = role_dropdown.get()
    url = data.get(selected_role)
    if url:
      return selected_role.strip()
    else:
      print(f"Invalid role selected: {selected_role}")

  role_dropdown = ttk.Combobox(window, values=list(data.keys()))
  role_dropdown.pack(pady=10)

  select_button = tk.Button(window, text="Select", command=handle_selection)
  select_button.pack(pady=10)

  window.mainloop()

# get_ib_roles()
website = ask_role()


class CrawlingSpider(CrawlSpider):
    name = "mycrawler"
    allowed_domains = ["interviewbit.com"]
    start_urls = [website]

    rules = {Rule(LinkExtractor(allow=website.replace("https://www.interviewbit.com/","")), callback="parse_ib")
    }

    def parse_ib(self, response):
        sections = response.xpath("//section[@class='ibpage-article-header']")

        for section in sections:
            question = section.xpath(".//h3/text()").get().strip()
            answer = section.xpath(".//article[@class='ibpage-article']/descendant-or-self::text()").getall()
            answer = " ".join(answer).strip()

            extracted_data = {
                "question": question,
                "answer": answer
            }
            yield extracted_data

driver.quit()
