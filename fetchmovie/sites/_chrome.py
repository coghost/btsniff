from selenium import webdriver


def init_driver():
    chrome_options = webdriver.ChromeOptions()
    # remove "chrome is being controlled by automated software"
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # disable "save password" popup
    prefs = {
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False,
    }
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_page_by_chrome(url):
    driver = init_driver()
    driver.get(url)
    dat = driver.page_source
    return dat
