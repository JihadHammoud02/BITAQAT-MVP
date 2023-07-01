from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time as t
import datetime
from datetime import datetime, timedelta, time

# Get the current date
current_date = datetime.now().date()

# Add one day to the current date
tomorrow_date = current_date + timedelta(days=1)

# Set the time to 12:00 PM
noon_time = time(12, 0)

# Combine the modified date and time
tomorrow_at_noon = datetime.combine(tomorrow_date, noon_time)

# Set the path to your ChromeDriver executable
chromedriver_path = ' chromedriver.exe'

# Set Chrome options
chrome_options = Options()
# Uncomment the following line to run Chrome in headless mode (without GUI)
# chrome_options.add_argument('--headless')

# Create a new ChromeDriver instance
driver = webdriver.Chrome(service=Service(
    chromedriver_path), options=chrome_options)

# Open your local Django website
driver.get('http://localhost:8000')


list_of_users = [
    {"email": "user1@gmail.com", "username": "user1", "password": "123"},
    {"email": "user2@gmail.com", "username": "user2", "password": "123"},
    {"email": "user3@gmail.com", "username": "user3", "password": "123"},
    {"email": "user4@gmail.com", "username": "user4", "password": "123"},
    {"email": "user5@gmail.com", "username": "user5", "password": "123"},
    {"email": "user6@gmail.com", "username": "user6", "password": "123"},
    {"email": "user7@gmail.com", "username": "user7", "password": "123"},
    {"email": "user8@gmail.com", "username": "user8", "password": "123"},
    {"email": "user9@gmail.com", "username": "user9", "password": "123"},
]


list_of_Games = [{"banner": r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\3472796-111116230.jpeg", "hteam": "Al Ahli Fc", "hteamlogo":  r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\Ahli.png", "ateam": "Al Nasr Fc",
                  "ateamlogo": r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\AlNasr.png", "Date": tomorrow_at_noon, "max": 200, "place": "Stadium", "price": 45, 'rr': 10},
                 {"banner": r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\3472796-111116230.jpeg", "hteam": "Al Ahli Fc", "hteamlogo":  r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\Ahli.png", "ateam": "Faysal Fc",
                  "ateamlogo": r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\faysal.png", "Date": tomorrow_at_noon, "max": 200, "place": "Stadium", "price": 45, 'rr': 10},
                 {"banner": r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\3472796-111116230.jpeg", "hteam": "Al Ahli Fc", "hteamlogo":  r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\Ahli.png", "ateam": "Hilal Fc",
                  "ateamlogo": r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\hilal.png", "Date": tomorrow_at_noon, "max": 200, "place": "Stadium", "price": 45, 'rr': 10},
                 {"banner": r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\3472796-111116230.jpeg", "hteam": "Al Ahli Fc", "hteamlogo":   r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\Ahli.png", "ateam": "Khaleej Fc",
                  "ateamlogo": r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\khaleej.png", "Date": tomorrow_at_noon, "max": 200, "place": "Stadium", "price": 45, 'rr': 10},
                 {"banner": r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\3472796-111116230.jpeg", "hteam": "Al Ahli Fc", "hteamlogo":  r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\Ahli.png", "ateam": "Al Ittihad",
                  "ateamlogo": r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\ittihad.png", "Date": tomorrow_at_noon, "max": 200, "place": "Stadium", "price": 45, 'rr': 10},
                 {"banner": r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\3472796-111116230.jpeg", "hteam": "Al Ahli Fc", "hteamlogo":   r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\Ahli.png", "ateam": "Al Raed Fc",
                  "ateamlogo": r"C:\Users\user\Desktop\NETSTUB\Tech\MVP\SOURCECODE\Bitaqat-MVP\Data\AlRaed.png", "Date": tomorrow_at_noon, "max": 200, "place": "Stadium", "price": 45, 'rr': 10}]


sign_in = driver.find_element(
    By.XPATH, '/html/body/header/div/div/div/div[2]/div/a[1]')
sign_in.click()

t.sleep(3)

username = driver.find_element(By.XPATH, '//*[@id="username"]')
username.send_keys("Ahlifc")
pwd = driver.find_element(By.XPATH, '//*[@id="exampleInputPassword1"]')
pwd.send_keys("Jihad2002")
login = driver.find_element(By.XPATH, '/html/body/div/form/button').click()

t.sleep(3)


create = driver.find_element(
    By.XPATH, '/html/body/header/div/div/div/div[2]/div/ul/li[3]/a')
create.click()

t.sleep(3)


for game in list_of_Games:
    banner = driver.find_element(By.XPATH, '//*[@id="Team1"]')
    banner.clear()
    banner.send_keys(game['banner'])
    hteam = driver.find_element(By.XPATH, '//*[@id="name1"]')
    hteam.clear()
    hteam.send_keys(game['hteam'])
    hlogo = driver.find_element(By.XPATH, '//*[@id="Teamh"]')
    hlogo.clear()
    hlogo.send_keys(game['hteamlogo'])
    ateam = driver.find_element(By.XPATH, '//*[@id="name2"]')
    ateam.clear()
    ateam.send_keys(game['ateam'])
    alogo = driver.find_element(By.XPATH, '//*[@id="Team2"]')
    alogo.clear()
    alogo.send_keys(game['ateamlogo'])
    max = driver.find_element(By.XPATH, '//*[@id="maxticket"]')
    max.clear()
    max.send_keys(game['max'])
    price = driver.find_element(By.XPATH, '//*[@id="price/ticket"]')
    price.clear()
    price.send_keys(game['price'])
    place = driver.find_element(By.XPATH, '//*[@id="inputCity"]')
    place.clear()
    place.send_keys(game['place'])
    rr = driver.find_element(By.XPATH, '//*[@id="royl"]')
    rr.clear()
    rr.send_keys(game['rr'])
    submit = driver.find_element(
        By.XPATH, '/html/body/div[3]/form/center/div/div/button')
    submit.click()
    t.sleep(3)


driver.quit()
