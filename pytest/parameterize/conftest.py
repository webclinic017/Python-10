import json
from pytest import fixture
from selenium import webdriver
from webdriver_manager import chrome

data_path = 'test_data.json'
chrome_driver_manager = chrome.ChromeDriverManager().install()


# firefox_driver = webdriver.Firefox(executable_path=firefox.GeckoDriverManager().install())
# edge_driver = webdriver.Edge(microsoft.EdgeChromiumDriverManager().install())

def load_test_data(path):
    with open(path) as data_file:
        data = json.load(data_file)
        return data

@fixture(scope="session", params=[chrome_driver_manager])
def browser(request):
    try:
        driver_manager = request.param
        driver = webdriver.Chrome(driver_manager)
        yield driver
    finally:
        # TearDown
        driver.quit()

@fixture(params=load_test_data(data_path))
def company(request):
    data = request.param
    return data
