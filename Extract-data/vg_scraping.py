import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

service = Service("D:/chromedriver-win64/chromedriver.exe")  # Update this!
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Open the VGInsights Gameloft publisher page
driver.get("https://vginsights.com/publisher/15194/gameloft")
sleep(5)  # Wait for page to load (can be replaced with WebDriverWait)

# Open a CSV file to write the results
csv_file = open('vginsights_gameloft_data1.csv', mode='w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
wait = WebDriverWait(driver, 10)    
# Write the header row
writer.writerow([
    'Game Name', 'Link', 'Active Players (now)', 'Active Players (24h peak)',
    'Positive Reviews', 'Units Sold', 'Avg Playtime', 'Median Playtime',
    'First Release Date', 'Current Price', 'Genres', 'Steam Tags',
    'Languages', 'Description'
])

def expand_steam_tags_languages_description(driver, wait):
    # Handles last 3 expandable parts: Steam Tags, Languages, Description
    button_texts = ["Show all", "See more"]

    for btn_text in button_texts:
        try:
            # Wait for all buttons with "Show all" or "See more"
            buttons = wait.until(EC.presence_of_all_elements_located(
                (By.XPATH, f"//button[.//span[contains(text(), '{btn_text}')]]")
            ))

            # Only click the LAST 3 of these buttons (tailored for your use case)
            for btn in buttons[-3:]:
                try:
                    btn.click()
                    print(f"Clicked button with text: {btn_text}")
                    time.sleep(0.5)  # allow time for content to expand
                except Exception as e:
                    print(f"Failed to click button: {e}")
        except:
            print(f"No button with text '{btn_text}' found.")



# Loop through first few games (or all)
for i in range(10,15):
    games = driver.find_elements(By.XPATH, '//base-name-cell/a')
    game = games[i]
    game_name = game.text
    game_link = game.get_attribute("href")

    print(f"Game: {game_name}")
    print(f"Link: {game_link}")

    # Visit the detail page
    driver.get(game_link)
    sleep(100)  # Wait for detail page to load

 
        # Active players (73 min ago)
    active_players_now = driver.find_element(
        By.XPATH, "//div[contains(text(), 'active players')]/preceding-sibling::h2"
    ).text
    print("Active Players (now):", active_players_now)

    # Active players (24h peak)
    active_players_24h = driver.find_element(
        By.XPATH, "//div[contains(text(), 'active players (24h peak)')]/preceding-sibling::h2"
    ).text
    print("Active Players (24h peak):", active_players_24h)

    # Positive reviews
    positive_reviews = driver.find_element(
        By.XPATH, "//div[contains(text(), 'positive reviews')]/preceding-sibling::h2"
    ).text
    print("Positive Reviews:", positive_reviews)


    # Units sold
    units_sold = driver.find_element(
        By.XPATH, "//div[contains(text(), 'units sold')]/preceding-sibling::h2"
    ).text
    print("Units Sold:", units_sold)

    # Avg playtime
    avg_playtime = driver.find_element(
        By.XPATH, "//div[contains(text(), 'avg playtime')]/preceding-sibling::h2"
    ).text
    print("Avg Playtime:", avg_playtime)

    # Median playtime
    median_playtime = driver.find_element(
        By.XPATH, "//div[contains(text(), 'median playtime')]/preceding-sibling::h2"
    ).text
    print("Median Playtime:", median_playtime)

    # First Release Date
    first_release_date = driver.find_element(
        By.XPATH, "//div[strong[contains(text(), 'First Release Date')]]"
    ).text.replace("First Release Date: ", "")
    print("First Release Date:", first_release_date)

   

    # Current Price
    current_price = driver.find_element(
        By.XPATH, "//div[strong[contains(text(), 'Current price')]]//span"
    ).text
    print("Current Price:", current_price)

    # Genres
    genres = driver.find_element(
        By.XPATH, "//div[strong[contains(text(), 'Genres')]]"
    ).text.replace("Genres: ", "")
    print("Genres:", genres)

    expand_steam_tags_languages_description(driver, wait)
    try:
        steam_tags = driver.find_element(
          By.XPATH, "//div[strong[contains(text(), 'Steam Tags')]]"
        ).text.replace("Steam Tags: ", "")
        print("Steam Tags:", steam_tags)
    except Exception as e:
        print("Steam Tags: Not found")

    # Languages
    try:
        languages = driver.find_element(
            By.XPATH, "//div[strong[contains(text(), 'Languages')]]"
        ).text.replace("Languages: ", "")
        print("Languages:", languages)
    except Exception as e:
        print("Languages: Not found")

    # Description
    try:
        description = driver.find_element(
            By.XPATH, "//div[strong[contains(text(), 'Description')]]"
        ).text
        print("Description:", description)
    except Exception as e:
        print("Description: Not found")

 
    # Example after getting all fields (with try-excepts like earlier)
    writer.writerow([
        game_name,
        game_link,
        active_players_now,
        active_players_24h,
        positive_reviews,
        units_sold,
        avg_playtime,
        median_playtime,
        first_release_date,
        current_price,
        genres,
        steam_tags,
        languages,
        description
    ])


    print("-" * 50)

    # Go back to main list
    driver.back()
    sleep(5)
csv_file.close()


# Close browser
driver.quit()
