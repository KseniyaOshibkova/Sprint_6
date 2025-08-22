from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def waiting_for_element(self, locator):
        """Ожидает заданный элемент"""
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator))
        return element

    def check_current_url(self, url):
        """Проверяет переход на главную страницу"""
        return self.driver.current_url == url

    def waiting_for_url(self, expected_url):
        """Ожидает заданный url"""
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be(expected_url))

    def find_elements(self, locator):
        """Ищет элемент по локатору"""
        by, value = locator
        return self.driver.find_elements(by, value)

    def find_element(self, locator):
        """Ищет элемент по локатору"""
        by, value = locator
        return self.driver.find_element(by, value)

    def scroll_for_element(self, element):
        """Скролит до элемиента"""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def click_element(self, locator, timeout=10):
        """Кликает по элементу"""
        element = WebDriverWait(self.driver, timeout).until(
                  EC.element_to_be_clickable(locator))
        element.click()

    def fill_input(self, locator, value):
        """Заполняет поле ввода"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(value)

    def fill_inputs(self, locators_and_values):
        """Заполняет поля ввода переданные в списке"""
        for locator, value in locators_and_values:
            self.fill_input(locator, value)

    def check_displayed_element(self, locator):
        """Проверяет отображение элемента"""
        element = self.waiting_for_element(locator)
        return element.is_displayed()

    def open_new_tab_and_get_url(self, click_locator):
        """Кликает по элементу, который открывает новую вкладку,
        переключается на неё и возвращает URL новой вкладки."""
        original_tab = self.driver.current_window_handle
        # кликнуть по кнопке
        self.click_element(click_locator)
        # переключиться на новую вкладку
        new_tab = [h for h in self.driver.window_handles if h != original_tab][0]
        self.driver.switch_to.window(new_tab)
        # Вернуть URL новой вкладки и оригинальной вкладки
        return self.driver.current_url, original_tab
