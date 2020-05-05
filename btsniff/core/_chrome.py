from selenium import webdriver
from aibot import AiBot


def init_driver(headless=True):
    chrome_options = webdriver.ChromeOptions()
    # remove "chrome is being controlled by automated software"
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # disable "save password" popup
    prefs = {
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False,
        'profile.default_content_setting_values': {
            'images': 2,
            'notifications': 2,
            'javascript': 0,
            'geolocation': 0,
        }
    }
    chrome_options.add_experimental_option('prefs', prefs)
    if headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_page_by_chrome(url):
    driver = init_driver()
    driver.get(url)
    dat = driver.page_source
    driver.quit()
    return dat


def search_by_chrome(url, params, headless=True):
    driver = init_driver(headless)
    aib = AiBot(driver)
    aib.get(url)
    selector, txt = params
    aib.update_text(selector, txt + '\n')
    aib.bot.switch_to_window(1)
    dat = aib.driver.page_source
    aib.driver.quit()
    return dat
