import pytest
from selenium import webdriver

from data.url import Url
from pages.order_page import OrderPage
from pages.questions_about_important_page import QuestionsAboutImportantPage


@pytest.fixture
def driver():
    # Фикстура создает экземпляр класса для каждого теста, открывает главную страницу, закрывает браузер
    driver = webdriver.Firefox()
    driver.get(Url.BASE_URL)
    yield driver
    driver.quit()

@pytest.fixture(scope='function', autouse=False)
def questions_about_important_page(driver):
    return QuestionsAboutImportantPage(driver)

@pytest.fixture(scope='function', autouse=False)
def order_page(driver):
    return OrderPage(driver)
