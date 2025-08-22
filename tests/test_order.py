import allure
import pytest
from data.data_for_order import DataForOrder
from pages.order_page import OrderPage


class TestOrder:
    """Тесты на проверку оформления заказа"""

    @allure.title('Оформление заказа самоката')
    @allure.description('Проходим полный позитивный сценарий оформления заказа с разными тестовыми данными и проверяем'
                        ' корректность url при переходах')
    @pytest.mark.parametrize("order_button_locator", [OrderPage.order_button_high, OrderPage.order_button_low])
    @pytest.mark.parametrize("case", DataForOrder.FULL_ORDER_TEST_DATA)
    def test_full_order_flow(self, driver, order_page, case, order_button_locator):
        """Проверка полного сценария заказа с разными точками входа"""
        with allure.step('Открыть форму заказа'):
            order_page.open_order_form(order_button_locator)

        with allure.step('Заполнить формы заказа'):
            order_page.fill_full_order_form(
                name=case["name"],
                surname=case["surname"],
                address=case["address"],
                phone=case["phone"],
                metro_station=case["metro"],
                date=case["date"],
                rent=case["rent"],
                color=case["color"],
                comment=case["comment"])

        with allure.step('Проверить переход по иконке самоката'):
            order_page.check_url_after_click_on_scooter()

        with allure.step('Проверить открытие Дзена через лого Яндекса'):
            order_page.check_open_dzen_after_click_on_yandex_logo()
