def send_email(msg):
    from dotenv import load_dotenv
    import os
    import requests
    import json
    load_dotenv()

    url = os.getenv("API_URL")
    email_to = os.getenv("EMAIL_TO")
    api_key=os.getenv("API_KEY")

    payload = json.dumps(
        {
            "sender": {"name": "Visa Alerts", "email": "alerts@alerts.com"},
            "to": [{"email": f"{email_to}"}],
            "subject": "Visa Alert",
            "textContent": msg,
        }
    )
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def get_visa_slots_html():
    from selenium import webdriver
    # Set up Selenium WebDriver (make sure to have the appropriate driver for your browser installed)
    # Here, I'm using Chrome as an example. You can use Firefox, Edge, etc., by changing the driver accordingly.
    driver = webdriver.Chrome()

    # URL to visit
    url = "https://visaslots.info/"

    try:

        # Open the webpage
        driver.get(url)
        
        # Wait for a while to ensure that the page is fully loaded (you might need to adjust the waiting time)
        driver.implicitly_wait(10)  # Wait for 10 seconds

        # Get the HTML content of the page
        html_content = driver.page_source

        # Print or process the HTML content as needed
        return html_content

    finally:
        # Close the browser
        driver.quit()

def fetch_earliest_slots_td_tags(html_doc):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_doc, 'html.parser')
    earliest_slot_td_tags = soup.find_all('figure')[2].find_all('td', class_='earliest')
    return earliest_slot_td_tags


def start_visa_alerts():
    import time
    while True: 
        visa_slots_html = get_visa_slots_html()
        td_tags = fetch_earliest_slots_td_tags(visa_slots_html)
        valid_slots = []

        for td_tag in td_tags:
            text = td_tag.text
            if "2024" in text and ("May" in text or "Jun" in text or "Jul" in text or "Sep" in text):
                for sibling in td_tag.next_siblings:
                    if not sibling.text.isspace():
                        valid_slots.append(text + "! Count: " + sibling.text + "\n\n")
                        break

        if len(valid_slots) > 0:
            msg = "The slots are" + "\n".join(valid_slots)
            send_email(msg)
        time.sleep(500)


start_visa_alerts()




