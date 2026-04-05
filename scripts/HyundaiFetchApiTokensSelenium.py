# hyundai_token_minimal.py
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import requests
import time
import os

# Find Chrome/Chromium
def find_chrome():
    paths = ['/usr/bin/chromium-browser', '/usr/bin/google-chrome', 
             '/usr/bin/google-chrome-stable', '/snap/bin/chromium']
    for path in paths:
        if os.path.exists(path):
            return path
    return None

CLIENT_ID = "6d477c38-3ca4-4cf3-9557-2a1929a94654"
CLIENT_SECRET = "KUy49XxPzLpLuoK0xhBC77W6VXhmtQR9iQhmIFjjoY4IpxsV"
BASE_URL = "https://idpconnect-eu.hyundai.com/auth/api/v2/user/oauth2/"

chrome_path = find_chrome()
if not chrome_path:
    print("Chrome/Chromium not found! Install with: sudo apt install chromium-browser")
    exit()

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 4.1.1; Galaxy Nexus Build/JRO03C) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19_CCS_APP_AOS")
options.binary_location = chrome_path
options.add_argument("--window-size=800,600")  # Smaller window
options.add_argument("--window-position=0,0")

try:
    driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
except:
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Login page
driver.get(f"{BASE_URL}authorize?client_id=peuhyundaiidm-ctb&redirect_uri=https%3A%2F%2Fctbapi.hyundai-europe.com%2Fapi%2Fauth&nonce=&state=PL_&scope=openid+profile+email+phone&response_type=code&connector_client_id=peuhyundaiidm-ctb&connector_scope=&connector_session_key=&country=&captcha=1&ui_locales=en-US")

print("\n" + "="*50)
print("LOGIN REQUIRED: Complete login and reCAPTCHA in browser")
print("="*50)
input("\nPress Enter AFTER successful login...")

# Get auth code
driver.get(f"{BASE_URL}authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=https://prd.eu-ccapi.hyundai.com:8080/api/v1/user/oauth2/token&lang=de&state=ccsp")
time.sleep(2)

match = re.search(r'code=([^&]+)', driver.current_url)
if match:
    code = match.group(1)
    response = requests.post(f"{BASE_URL}token", data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://prd.eu-ccapi.hyundai.com:8080/api/v1/user/oauth2/token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })
    
    if response.status_code == 200:
        token = response.json().get("refresh_token")
        print(f"\n{'='*60}\n✅ REFRESH TOKEN:\n{token}\n{'='*60}")
        print("Use this as PASSWORD in Home Assistant!")
    else:
        print(f"Error: {response.text}")
else:
    print("No code found in URL")

driver.quit()