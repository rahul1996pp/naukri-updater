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


bright = Style.BRIGHT
green, blue, red, cyan, reset = Fore.GREEN + bright, Fore.BLUE + bright, Fore.RED + bright, Fore.CYAN, Fore.RESET
init(convert=True, autoreset=True)

def process():
    options = Options()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2')
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(service=Service("chromedriver.exe"),options=options)
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

def resume_checker():
    if not (glob("*.pdf") + glob("*.docx")):
        print(f"{red}[-] Put resume file in the folder")
        input()
        exit()
    else:
        print(f"{green}[+] Resume found")

def login_details():
    global data
    data = ConfigObj('data.txt')
    if not exists('data.txt'):
        print(f"{green}[+] creating file to store data")
        open("data.txt", "w").write("email=\npassword=")
        data = ConfigObj('data.txt')
    if not (data['email'] or data['password']):
        data['email']=input("[+] Enter your email address = ")
        data['password']=input("[+] Enter password = ")
        data.write()
    else:
        print(f"{green}[+] username and password found")


def credit():
    credit_text = f"""
               {red}NAUKRI UPDATER
{green}               
     ██▀███   ▄▄▄       ██░ ██  █    ██  ██▓    
    ▓██ ▒ ██▒▒████▄    ▓██░ ██▒ ██  ▓██▒▓██▒    
    ▓██ ░▄█ ▒▒██  ▀█▄  ▒██▀▀██░▓██  ▒██░▒██░    
    ▒██▀▀█▄  ░██▄▄▄▄██ ░▓█ ░██ ▓▓█  ░██░▒██░    
    ░██▓ ▒██▒ ▓█   ▓██▒░▓█▒░██▓▒▒█████▓ ░██████▒
    ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░ ▒ ░░▒░▒░▒▓▒ ▒ ▒ ░ ▒░▓  ░
      ░▒ ░ ▒░  ▒   ▒▒ ░ ▒ ░▒░ ░░░▒░ ░ ░ ░ ░ ▒  ░
      ░░   ░   ░   ▒    ░  ░░ ░ ░░░ ░ ░   ░ ░   
       ░           ░  ░ ░  ░  ░   ░         ░  ░ {blue}code generated by Rahul.p\n
    """
    print(credit_text)


def main():
    resume_checker()
    login_details()
    try:
        process()
    except TimeoutError:
        print(f"[-] Timeout submitting the resume again")
        process()

try:
    credit()
    main()
    print(f"{green}[+] Successfully uploaded")
    input()
except KeyboardInterrupt:
    print(f'{red}\n[~] Exiting ....')
except Exception as e:
    print(f"{red}\n[-] error message is {e}")
