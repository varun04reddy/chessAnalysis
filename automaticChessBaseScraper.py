from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re

def scrape_games(driver, url):
    driver.get(url)
    time.sleep(3)

    game_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/perl/chessgame?gid=']")
    game_data = []

    for link in game_links:
        href = link.get_attribute('href')
        driver.get(href)
        time.sleep(2)
        game_text_element = driver.find_element(By.ID, 'olga-data') # timing out right here - look into the find_element call
        game_text = game_text_element.text
        game_data.append(game_text)

    return game_data

def save_to_pgn(game_data, file_name):
    with open(file_name, 'w') as file:
        for game in game_data:
            file.write(game + "\n\n")

def main():
    url = 'https://www.chessgames.com/perl/chess.pl?tid=91599'
    path_to_driver = '/Users/varun/WebDrivers/chromedriver'
    driver = webdriver.Chrome(executable_path=path_to_driver)

    try:
        game_data = scrape_games(driver, url)
        save_to_pgn(game_data, 'magnus_carlsen_tournament_games.pgn')
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
