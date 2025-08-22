import allure
import pytest
from data.data_for_questions import DataForQuestions




class TestQuestionsAboutImportant:
    """Тесты на проверку раздела о важном"""

    @allure.title('Ответы на вопросы в разделе "Вопросы о важном"')
    @allure.description('Проверяем соответствие ответов вопросам')
    @pytest.mark.parametrize("test_data",DataForQuestions.FAQ_TEST_DATA)
    def test_faq_answer(self, driver, questions_about_important_page, test_data):
        with allure.step('Открыть ответ на вопрос и проверить содержание'):
            questions_about_important_page.check_answer(
            question_text=test_data["question"],
            expected_answer=test_data["expected_answer"])
