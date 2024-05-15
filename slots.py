def get_visa_slots_html():
    from selenium import webdriver
    # Set up Selenium WebDriver (make sure to have the appropriate driver for your browser installed)
    # Here, I'm using Chrome as an example. You can use Firefox, Edge, etc., by changing the driver accordingly.
    options = webdriver.ChromeOptions()
    #options.binary_location ='/usr/bin/chromedriver'
    options.add_argument('--headless')
    service = webdriver.ChromeService(executable_path = '/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)


    # driver = webdriver.Chrome('usr/lib/chromium-browser/chromedriver')

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
    import pygame
    import datetime
    import pytz
    while True: 
        visa_slots_html = get_visa_slots_html()
        td_tags = fetch_earliest_slots_td_tags(visa_slots_html)
        valid_slots = []

        for td_tag in td_tags:
            text = td_tag.text
            if "2024" in text and ("May" in text or "Jun" in text or "Jul" in text):
                india_tz = pytz.timezone("Asia/Kolkata")
                india_time = datetime.datetime.now(india_tz)
                india_time = india_time.strftime("%H:%M:%S")


                append_text = text + f'{india_time}'
                for sibling in td_tag.next_siblings:
                    if not sibling.text.isspace():
                        append_text += "\nCount: " + sibling.text + "\n\n"
                        break
                valid_slots.append(append_text)

        if len(valid_slots) > 0:
            print("Valid slots found...")
            msg = "The slots are" + "\n".join(valid_slots)
            print(msg)
            pygame.init()
            sound = pygame.mixer.Sound('./alert')
            sound.play(loops=3)
        else:
            print("Valid slots not found...")
        print("Sleeping...")
        time.sleep(180)


start_visa_alerts()




