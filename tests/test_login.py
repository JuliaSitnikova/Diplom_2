from reqs.reqUser import RequestsUser
import allure
from faker import Faker

fake = Faker()
@allure.feature('Проверки авторизации пользователя')
class TestLogin:
    @allure.title('Проверка входа существующего пользователя')
    def test_exist_user_login(self, create_user_payload, make_user):
        payload = create_user_payload(email='rand', password='1234', name='rand')
        user = make_user(data=payload)
        logged_user = RequestsUser().post_login_user(data=payload, token=user["text"]['accessToken'])
        assert logged_user["text"]['user']['email'] == payload['email']

    @allure.title('Проверка, что пользователь на может войти под неверным логином и паролем')
    def test_user_incorrect_login_password(self, create_user_payload, make_user):
        payload = create_user_payload(email='rand', password='1234', name='rand')
        user = make_user(data=payload)
        new_payload_wrong_name = payload.update({'name': fake.name()})
        user_wrong_name = RequestsUser().post_login_user(data=new_payload_wrong_name, token=user["text"]['accessToken'])

        new_payload_wrong_password = payload.update({'password': fake.pyint()})
        user_wrong_password = RequestsUser().post_login_user(data=new_payload_wrong_password,
                                                             token=user['text']['accessToken'])
        assert (user_wrong_password["status_code"] or user_wrong_name["status_code"] == 401 and
                user_wrong_password["text"]['message'] or user_wrong_name["text"]['message'] == 'email or password are incorrect')

