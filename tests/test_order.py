import allure
import pytest
from reqs.reqOrder import RequestsOrder
from faker import Faker

fake = Faker()

@allure.feature('Проверки создания заказа')
class TestOrders:

    @allure.title('Проверка создания заказа с токеном пользователя и ингредиентами')
    def test_create_order_authorized_user(self, create_order_payload, make_user, create_user_payload):
        user_payload = create_user_payload(email='rand', password='rand', name='rand')
        user = make_user(data=user_payload)
        order_payload = create_order_payload
        token = user["text"]['accessToken']
        resp = RequestsOrder().post_create_order(data=order_payload, token=token)
        assert resp['status_code'] == 200 and resp["text"]["success"]
    @allure.title('Проверка создания заказа без токена пользователя и ингредиентами')
    def test_create_order_not_authorized_user(self, create_order_payload):
        payload = create_order_payload
        resp = RequestsOrder().post_create_order_without_token(data=payload)
        assert resp['status_code'] == 200 and resp["text"]["success"]

    @allure.title('Проверка, что нельзя создать заказ с неверным id ингредиента')
    def test_create_order_incorrect_id(self, create_order_payload):
        payload = create_order_payload
        payload["ingredients"][0] = payload["ingredients"][0] + str(fake.pyint())
        resp = RequestsOrder().post_create_order_without_token(data=payload)
        assert resp['status_code'] == 500 and 'Internal Server Error' in resp["text"]

    @allure.title('Нельзя создать заказ с токеном и неверным id ингредиента')
    def test_create_order_token_incorrect_id(self, create_order_payload, create_user_payload,
                                             make_user):
        user_payload = create_user_payload(email='rand', password='rand', name='rand')
        user = make_user(data=user_payload)
        token = user["text"]['accessToken']
        payload = create_order_payload
        payload["ingredients"][0] = payload["ingredients"][0] + str(fake.pyint())
        resp = RequestsOrder().post_create_order(data=payload, token=token)
        assert resp['status_code'] == 500 and 'Internal Server Error' in resp["text"]

    @allure.title('Проверка, что нельзя создать заказ без ингредиента')
    def test_create_order_without_ingredients(self):
        payload = {}
        resp = RequestsOrder().post_create_order_without_token(data=payload)
        assert resp['status_code'] == 400 and resp["text"]["message"] == 'Ingredient ids must be provided'

    @allure.title('Проверка, что нельзя создать заказ с токеном и без ингредиента')
    def test_create_order_token_without_ingredients(self, make_user, create_user_payload):
        user_payload = create_user_payload(email='rand', password='rand', name='rand')
        user = make_user(data=user_payload)
        token = user["text"]['accessToken']
        payload = {}
        resp = RequestsOrder().post_create_order(data=payload, token=token)
        assert resp['status_code'] == 400 and resp["text"]["message"] == 'Ingredient ids must be provided'

