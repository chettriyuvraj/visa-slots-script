def send_whatsapp_alert(valid_slots):
    import pywhatkit
    msg = "Valid slots available for: " + " ".join(valid_slots)
    pywhatkit.sendwhatmsg_instantly("+919819085080", "this is a test message", 80, True, 4)
    

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


visa_slots_html = get_visa_slots_html()
td_tags = fetch_earliest_slots_td_tags(visa_slots_html)
valid_slots = []

for td_tag in td_tags:
    text = td_tag.text
    if "2024" in text and ("May" in text or "Jun" in text or "Jul" in text or "Sep" in text):
        valid_slots.append(text)

if len(valid_slots) > 0:
    print(valid_slots)
    send_whatsapp_alert(valid_slots)
