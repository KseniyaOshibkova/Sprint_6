from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from data.url import Url
from selenium.webdriver.common.keys import Keys


class OrderPage(BasePage):
    order_button_high = (By.XPATH, "//div[contains(@class, 'Header_Nav')]//button[contains(@class, 'Button_Button') "
                                   "and text()='Заказать']")
    order_button_low = (By.XPATH, "//div[contains(@class, 'Home_FinishButton')]//button[contains(@class, "
                                  "'Button_Button') and text()='Заказать']")
    order_button_in_form = (By.XPATH, "//button[contains(@class, 'Button_Button') and contains(@class, 'Button_Middle')"
                                      " and text()='Заказать']")
    name_input = (By.XPATH, "//input[contains(@class, 'Input_Input') and @placeholder='* Имя']")
    surname_input = (By.XPATH, "//input[contains(@class, 'Input_Input') and @placeholder='* Фамилия']")
    address_input = (By.XPATH, "//input[contains(@class, 'Input_Input') and @placeholder='* Адрес: куда привезти "
                              "заказ']")
    metro_drop_down = (By.XPATH, "//input[contains(@class, 'select-search__input') and @placeholder='* Станция метро']")
    phone_input = (By.XPATH, "//input[contains(@class, 'Input_Input') and @placeholder='* Телефон: на него позвонит "
                              "курьер']")
    next_button = (By.XPATH, "//button[contains(@class, 'Button_Button') and text()='Далее']")
    metro_options = (By.CSS_SELECTOR, "ul.select-search__options li button.select-search__option")
    calendar_for_rent = (By.XPATH, "//input[contains(@class, 'Input_Input') and @placeholder='* Когда привезти "
                                   "самокат']")
    rental_period_drop_down = (By.XPATH, "//div[text()='* Срок аренды']/ancestor::div[@class='Dropdown-control']")
    rental_period_option = (By.XPATH, "//div[@class='Dropdown-menu']/div[text()='{}']")
    checkbox_color = (By.XPATH, "//div[contains(@class, 'Order_Checkboxes__3lWSI')]//label[contains(text(), "
                                "'{}')]/input")
    comment_for_courier_input = (By.XPATH, "//input[contains(@class, 'Input_Input') and @placeholder='Комментарий для "
                                           "курьера']")
    modal_window_order = (By.XPATH, "//div[contains(text(), 'Хотите оформить заказ?')]/ancestor::div[contains(@class,"
                                    " 'Order_Modal')]")
    yes_button = (By.XPATH, "//div[contains(@class, 'Order_Modal')]//button[text()='Да']")
    scooter_button = (By.XPATH, "//a[contains(@class, 'Header_LogoScooter') and "
                                          ".//img[@src='/assets/scooter.svg' and @alt='Scooter']]")
    yandex_logo = (By.XPATH, "//a[contains(@class, 'Header_LogoYandex')]")
    order_modal = (By.XPATH, "//div[contains(@class, 'Order_Modal')]//div[contains(text(), 'Заказ оформлен')]")
    view_status_button = (By.XPATH, "//button[text()='Посмотреть статус']")

    def __init__(self, driver):
        super().__init__(driver)

    def open_order_form(self, order_button_locator):
        """Открывает форму заказа"""
        element = self.find_element(order_button_locator)
        self.scroll_for_element(element)
        self.click_element(order_button_locator)
        self.waiting_for_url(Url.ORDER_PAGE)

    def fill_order_form(self, name, surname, address, phone, metro_station):
        """Заполняет форму заказа и кликает Далее"""
        self.fill_inputs([
            (self.name_input, name),
            (self.surname_input, surname),
            (self.address_input, address),
            (self.phone_input, phone)])
        self.select_metro_station(metro_station)
        self.click_element(self.next_button)

    def select_metro_station(self, metro_station):
        """Выбирает станцию метро из выпадающего списка"""
        self.click_element(self.metro_drop_down)  # раскрываем список
        options = self.find_elements(self.metro_options)
        for option in options:
            if option.text.strip() == metro_station:
                option.click()
                break

    def select_date(self, date_text):
        """Выбирает дату через календарь"""
        element = self.find_element(self.calendar_for_rent)
        element.clear()
        element.send_keys(date_text)
        element.send_keys(Keys.ENTER)

    def select_rental_period(self, period_text):
        """Выбирает срок аренды"""
        self.click_element(self.rental_period_drop_down)
        option_locator = (self.rental_period_option[0], self.rental_period_option[1].format(period_text))
        self.click_element(option_locator)


    def fill_rent_form(self, date, rent, color, comment):
        """Заполняет форму аренды"""
        self.select_date(date)
        self.select_rental_period(rent)
        self.select_checkbox_by_text(self.checkbox_color, color)
        self.fill_input(self.comment_for_courier_input, comment)

    def select_checkbox_by_text(self, locator_template, label_text):
        """Кликает по чекбоксу, подставляя цвет самоката"""
        locator = (locator_template[0], locator_template[1].format(label_text))
        element = self.waiting_for_element(locator)
        if not element.is_selected():
            element.click()

    def fill_full_order_form(self, name, surname, address, phone, metro_station, date, rent, color, comment):
        """Заполняет все шаги формы заказа и отправляет заказ"""
        self.fill_order_form(name, surname, address, phone, metro_station)
        self.fill_rent_form(date, rent, color, comment)
        self.click_element(self.order_button_in_form)
        self.waiting_for_element(self.modal_window_order)
        self.click_element(self.yes_button)
        self.check_displayed_element(self.order_modal)
        self.click_element(self.view_status_button)

    def check_url_after_click_on_scooter(self):
        """Проверяет url после клика по иконке самоката"""
        self.click_element(self.scooter_button)
        self.check_current_url(Url.BASE_URL)

    def check_open_dzen_after_click_on_yandex_logo(self):
        """Проверяет, что после клика по лого Яндекса открывается новая вкладка Дзен"""
        new_tab_url, original_tab = self.open_new_tab_and_get_url(self.yandex_logo)
        # закрываем новую вкладку и возвращаемся
        self.driver.close()
        self.driver.switch_to.window(original_tab)
        return new_tab_url == Url.DZEN
