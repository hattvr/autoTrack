# Auto Tracking Calculator
import configparser, time, warnings, os, threading, sys, selenium
from colorama import Fore
from configparser import ConfigParser
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import wait
from selenium.webdriver.support.expected_conditions import element_located_selection_state_to_be, presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from setuptools import setup

# Read config file and grab username/password
config = ConfigParser()
config.read('config.ini')
Xcoord = config.get('data','Xcoord').split(',')
Zcoord = config.get('data','Zcoord').split(',')
x = int(config.get('data','x'))
z = int(config.get('data','z'))
username = config.get('discord','username')
password = config.get('discord','password')
channel = config.get('discord','channel')
narrow = int(int(config.get('data','narrow'))/2)
theNarrow = config.get('data','narrow')
tracks = open("tracks.txt", "a")

# Disable python logging to console
warnings.filterwarnings("ignore")
clear = lambda: os.system('cls')
clear()
# Setup web-driver
options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--hide-scrollbars')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--log-level=3')
options.add_argument('--disable-infobars')
options.add_argument('--start-maximized')
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-extensions")
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
clear()

# TODO

class User:
    def login(self):
        try:
            driver.get(channel)
            time.sleep(1)
            driver.find_element_by_name('email').send_keys(username)
            driver.find_element_by_name('password').send_keys(password)
            driver.find_element_by_css_selector("[type=submit]").click()

            wait = WebDriverWait(driver, 300)
            wait.until(presence_of_element_located((By.CLASS_NAME, 'toolbar-3_r2xA')))
        except Exception as e:
            print(e)
            time.sleep(60)

    def setup(self):
        for i in range(0, len(Xcoord)):
            print(f"{Fore.WHITE}[{Fore.GREEN}Tracker {i+1}{Fore.WHITE}] {Fore.RESET}")
            print(Xcoord[i])
            print(Zcoord[i])
    
    def calculate(self):
        track.setup()

        # First Narrow
        try:
            tracker1 = input("\nFirst Tracker: ")
            x1 = int(Xcoord[int(tracker1)-1])
            z1 = int(Zcoord[int(tracker1)-1])
            narrowOne = int(input("First Narrow: "))
            directionOne = input("Direction of Narrow (n, e, s, w): ")
            if directionOne != "n" and directionOne != "e" and directionOne != "s" and directionOne != "w":
                print("Invalid Input! Please try again!")
                track.calculate()
                return
        except Exception as error:
            print(error)
            track.calculate()

        if directionOne != "n" and directionOne != "e" and directionOne != "s" and directionOne != "w":
            print("Invalid Input! Please try again!")
            track.calculate()
        
        # Second Narrow
        try:
            tracker2 = input("Second Tracker: ")
            x2 = int(Xcoord[int(tracker2)-1])
            z2 = int(Zcoord[int(tracker2)-1])
            narrowTwo = int(input("Second Narrow: "))
            directionTwo = input("Direction of Narrow (n, e, s, w): ")
            if directionTwo != "n" and directionTwo != "e" and directionTwo != "s" and directionTwo != "w":
                print("Invalid Input! Please try again!")
                track.calculate()
                return
            
        except Exception as error:
            print(error)
            track.calculate()
        

        # west=x- north=z- east=x+ south=z+
        if directionOne == "n":
            holdz = narrowOne - narrow
            z = z1 - holdz
        if directionOne == "e":
            holdx = narrowOne - narrow
            x = x1 + holdx
        if directionOne == "s":
            holdz = narrowOne - narrow
            z = z1 + holdz
        if directionOne == "w":
            holdx = narrowOne - narrow
            x = x1 - holdx

        if directionTwo == "n":
            holdz = narrowTwo - narrow
            z = z2 - holdz
        if directionTwo == "e":
            holdx = narrowTwo - narrow
            x = x2 + holdx
        if directionTwo == "s":
            holdz = narrowTwo - narrow
            z = z2 + holdz
        if directionTwo == "w":
            holdx = narrowTwo - narrow
            x = x2 - holdx


        p1 = (f"{Fore.RED}Overworld{Fore.RESET}: x:" + str(x) + " z:" + str(z))
        p2 = (f"{Fore.RED}Nether{Fore.RESET}: x:" + str(x/8) + " z:" + str(z/8))
        p3 = (f"{Fore.CYAN}(400 narrow){Fore.RESET}")
        print(p1, p2, p3)
        doLog = input("Would you like to log this track? ")
        logtxt = f"**Overworld:** x:" + str(x) +" z:" + str(z) + " **Nether:** x:" + str(x/8) + " z:" + str(z/8) + " (__"+theNarrow+" narrow__)\n"
        if doLog == "yes":
            name = input("Name of victim: ")
            try:
                driver.find_element_by_xpath('//*[@id="app-mount"]/div[2]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/main/form/div/div/div/div[1]/div/div[3]/div[2]/div').send_keys(name, " // ", logtxt, Keys.ENTER)
                time.sleep(10)
            except Exception as error:
                print(error)

        tracks.write(logtxt)
        track.calculate()
        print("\n")

                
# Set user details
track = User()
print(f"[+] {Fore.LIGHTCYAN_EX}Logging in...{Fore.RESET}")
track.login()
print(f"[+] {Fore.LIGHTCYAN_EX}Logged in!{Fore.RESET}")
# track.setup()
track.calculate()
