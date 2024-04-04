import allure
from reqs.reqOrder import RequestsOrder
from reqs.reqUser import RequestsUser

@allure.feature('Проверки создания заказов')
class TestOrderUser:

    @allure.title('Получение списка заказов неавторизованного пользователя')
    def test_get_orders_not_authorized_user(self, make_user, create_order_payload, create_user_payload):
        user_payload = create_user_payload(email='rand', password='rand', name='rand')
        user = make_user(data=user_payload)
        order_payload = create_order_payload
        token = user["text"]['accessToken']
        order = RequestsOrder().post_create_order(data=order_payload, token=token)
        resp = RequestsOrder().get_user_orders(token=token)
        assert order["status_code"] == 200 and order["text"]["order"]["number"] == resp["text"]["orders"][0]["number"]
    @allure.title('Получение списка заказов уже авторизованного пользователя')
    def test_get_orders_authorized_user(self, make_user, create_order_payload, create_user_payload):
        user_payload = create_user_payload(email='rand', password='rand', name='rand')
        user = make_user(data=user_payload)
        logged_user = RequestsUser().post_login_user(data=user_payload, token=user["text"]['accessToken'])
        order_payload = create_order_payload
        token = logged_user["text"]['accessToken']
        order = RequestsOrder().post_create_order(data=order_payload, token=token)
        resp = RequestsOrder().get_user_orders(token=token)
        assert order["text"]["order"]["number"] == resp["text"]["orders"][0]["number"]

    @allure.title('Получение списка заказов без токена')
    def test_get_orders_without_token(self, make_user, create_order_payload, create_user_payload):
        user_payload = create_user_payload(email='rand', password='rand', name='rand')
        user = make_user(data=user_payload)
        order_payload = create_order_payload
        token = user["text"]['accessToken']
        RequestsOrder().post_create_order(data=order_payload, token=token)
        resp = RequestsOrder().get_user_orders(token=None)
        assert resp["status_code"] == 401 and resp["text"]["message"] == "You should be authorised"