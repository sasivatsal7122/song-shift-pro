from selenium.webdriver.firefox.options import Options
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import undetected_chromedriver as uc

from fuzzywuzzy import fuzz

import time
import random

appleUrl = "https://music.apple.com/in/browse"

def getDriver():
    driver = uc.Chrome(headless=False,use_subprocess=True)
    return driver

driver = getDriver()
driver.get(appleUrl)

signIn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.signin.svelte-xupt29"))
)
signIn.click()
driver.switch_to.frame(driver.find_element(By.ID, "modal-body"))
username = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "accountName"))
)
ActionChains(driver).move_to_element(username).click()
username.send_keys('sasivatsal7122@gmail.com')
ActionChains(driver).send_keys(Keys.RETURN).perform()

password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "password_text_field"))
)
ActionChains(driver).move_to_element(password).click()
password.send_keys("Ap31et@0975")
ActionChains(driver).send_keys(Keys.RETURN).perform()
time.sleep(10)


import pickle
songNames = pickle.load(open('songInfo.pkl', 'rb'))


def searchSong(driver, songName):
    action = ActionChains(driver)
    search_input = driver.find_element(By.CLASS_NAME, 'search-input__text-field')
    ActionChains(driver).move_to_element(search_input).click()
    search_input.clear();time.sleep(3)
    action.send_keys(songName)
    action.send_keys(Keys.RETURN).perform()
    time.sleep(3)
    return

def addSongtoPlaylist(driver, targetCard):
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(targetCard.find_element(By.CSS_SELECTOR, "span[data-testid='more-button']"))
    )
    moreButton = targetCard.find_element(By.CSS_SELECTOR, "span[data-testid='more-button']")
    moreButton
    time.sleep(2)
    
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(targetCard.find_element(By.CSS_SELECTOR, "button[title='Add to Playlist']"))
    )
    add_to_playlist_button = targetCard.find_element(By.CSS_SELECTOR, "button[title='Add to Playlist']")
    add_to_playlist_button
    time.sleep(2)
    
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(targetCard.find_element(By.CSS_SELECTOR, "button[title='test']"))
    )
    myPlaylist = targetCard.find_element(By.CSS_SELECTOR, "button[title='test']")
    myPlaylist
    time.sleep(2)
    return

def find_best_match_card(driver, listCards, target_string):
    best_match_card = None
    best_score = -1

    for listCard in listCards[:2]:  
        songInfo = listCard.find_element(By.CSS_SELECTOR, "div[data-testid='top-search-result']").get_attribute("aria-label")
        songTitle = ' '.join(songInfo.split())
        if "Song" in songTitle:
            similarity_ratio = fuzz.ratio(target_string, songTitle)
            print(target_string, songTitle, similarity_ratio)

            if similarity_ratio > best_score:
                best_score = similarity_ratio
                best_match_card = listCard

    addSongtoPlaylist(driver, best_match_card)

ERROR_SONGS = []

for songName in songNames[450:500]:
    #try:
    print(f'Searching Song -> {songName}')

    searchSong(driver,songName)

    WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.section.svelte-1sdb5su[aria-label='Top Results']"))
    )
    topResults = driver.find_element(By.CSS_SELECTOR, "div.section.svelte-1sdb5su[aria-label='Top Results']")
    listCards = topResults.find_elements(By.CSS_SELECTOR, "li[data-testid='grid-item']")

    find_best_match_card(driver, listCards, songName) 
    # except:
    #     driver.refresh()
    time.sleep(random.randint(15,20))


