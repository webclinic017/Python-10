from pytest import fixture
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


chrome_driver = ChromeDriverManager().install()


@fixture(scope="session") # session
def chrome_browser():
    browser =  webdriver.Chrome(chrome_driver)
    yield browser

    # TearDown
    print("Close Chrome browser")
    browser.quit()
