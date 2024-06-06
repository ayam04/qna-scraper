import os
import json
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ib_url = "https://www.interviewbit.com/technical-interview-questions/"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--diable-cookies")

driver = webdriver.Chrome(options=options)

roles = {}

def get_ib_roles():
    print("Getting  Roles..")
    
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
    if not os.path.exists("roles.json"):
        print("Roles file not found. Please run get_ib_roles() first.")
        return None

    window = tk.Tk()
    window.title("Select Interview Role")
    
    selected_url = tk.StringVar()

    def handle_selection(event=None):
        selected_role = role_dropdown.get().strip()
        url = data.get(selected_role)
        if url:
            selected_url.set(url)
            window.destroy()
        else:
            print(f"Invalid role selected: {selected_role}")

    with open("roles.json") as f:
        data = json.load(f)

    role_dropdown = ttk.Combobox(window, values=list(data.keys()))
    role_dropdown.pack(pady=10)

    select_button = tk.Button(window, text="Select", command=handle_selection)
    select_button.pack(pady=10)

    window.mainloop()
    
    return selected_url.get()

def extract_ib_roles(website):
  filename = website.replace("https://www.interviewbit.com/","").replace("-questions/","").replace("-interview","")
  print("Extracting questions..")
  driver.get(website)
  sections = driver.find_elements(By.CLASS_NAME, "ibpage-article-header")
  extracted_data = []
  for section in sections:
      question = section.find_element(By.TAG_NAME, "h3").text.strip()
      answer_elements = section.find_element(By.CLASS_NAME, "ibpage-article")
      answer_text = [element.text.strip() for element in answer_elements.find_elements(By.XPATH, ".//*")]
      answer = " ".join(a.strip() for a in answer_text)


      extracted_data.append({
        "question": question,
        "answer": answer
      })
  try:
      with open(f"Outputs/{filename}.json","x", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)
  except FileExistsError:
      with open(f"Outputs/{filename}.json","w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)
  
  driver.close()

get_ib_roles()
website = ask_role()
extract_ib_roles(website)