from selenium.webdriver.common.by import By
from pages.base_page import BasePage



class QuestionsAboutImportantPage(BasePage):
    question_button = (By.XPATH, "//div[@class='accordion__button' and text()='{}']")
    answer_panel = (By.ID, "{}")
    answer_text = (By.TAG_NAME, "p")
    all_question_button = (By.CLASS_NAME, "accordion__button")

    def __init__(self, driver):
        super().__init__(driver)

    def get_answer(self, question_text):
        """Возвращает текст ответа для заданного вопроса
            question_text: Текст вопроса, который ищем в FAQ"""
        # Сформировать локатор кнопки вопроса
        locator = (self.question_button[0], self.question_button[1].format(question_text))
        # Найти кнопку
        question_button = self.find_element(locator)
        # Скролить до кнопки
        self.scroll_for_element(question_button)
        # Найти кнопку с нужным вопросом
        question_button = self.driver.find_element(*locator)
        # Кликнуть по кнопке, чтобы раскрыть ответ
        question_button.click()
        # Получить ID панели с ответом
        panel_id = question_button.get_attribute("aria-controls")
        # Дождаться появления панели с ответом
        panel = self.waiting_for_element((By.ID, panel_id))
        # Извлечь текст ответа
        return panel.find_element(*self.answer_text).text

    def check_answer(self, question_text, expected_answer):
        """Проверяет, что ответ на вопрос в FAQ соответствует ожидаемому
            question_text: Вопрос
            expected_answer: Текст, который должен быть в ответе"""
        # Получить фактический ответ со страницы
        actual_answer = self.get_answer(question_text)
        # Сравнить фактический ответ с ожидаемым
        assert actual_answer == expected_answer, (
            f"\nОшибка в FAQ для вопроса: '{question_text}'\n"
            f"Ожидалось: {expected_answer}\n"
            f"Получено: {actual_answer}")
