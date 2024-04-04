import pytest
import allure

from reqs.reqUser import RequestsUser


@allure.feature('Проверки создания пользователя')
class TestCreateUser:
    @allure.title('Проверка, что можно создать пользователя со случайным логином')
    def test_create_user(self, create_user_payload, del_user):
        payload = create_user_payload(email='rand', password='1234', name='rand')
        user = RequestsUser().post_create_user(data=payload)
        del_user.update({'token': user["text"]['accessToken']})
        assert user["status_code"] == 200 and user["text"]["success"]

    @allure.title('Проверка, что нельзя создать двух пользователей с одинаковыми логинами')
    def test_create_user_same_login(self, create_user_payload, make_user):
        payload = create_user_payload(email='rand', password='1234', name='rand')
        make_user(data=payload)
        resp_dupe = RequestsUser().post_create_user(data=payload)
        assert resp_dupe["status_code"] == 403 and resp_dupe["text"]["message"] == "User already exists"

    @pytest.mark.parametrize("payload_schema",
                             [
                                 [None, 'rand', 'rand'],
                                 ['rand', None, 'rand'],
                                 ['rand', 'rand', None]
                             ])
    @allure.title('Проверка обязательности полей для создания пользователя -email, имя, пароль')
    def test_required_field(self, payload_schema, create_user_payload):
        payload = create_user_payload(email=payload_schema[0], password=payload_schema[1],
                                      name=payload_schema[2])
        resp = RequestsUser().post_create_user(data=payload)
        assert resp["status_code"] == 403 and resp["text"]["message"] == "Email, password and name are required fields"