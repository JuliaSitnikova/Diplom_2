import requests
class RequestsBase:

    def post_request_with_token(self, url, data, token):
        headers = {'authorization': token}
        response = requests.post(url=url, data=data, headers=headers)
        if 'application/json' in response.headers['Content-Type']:
            return {"status_code": response.status_code, "text": response.json()}
        else:
            return {"status_code": response.status_code, "text": response.text}

    def post_request(self, url, data):
        response = requests.post(url=url, data=data)
        if 'application/json' in response.headers['Content-Type']:
            return {"status_code": response.status_code, "text": response.json()}
        else:
            return {"status_code": response.status_code, "text": response.text}

    def delete_request(self, url, token):
        headers = {"Content-Type": "application/json", 'authorization': token}
        response = requests.delete(url=url, headers=headers)
        return {"status_code": response.status_code, "text": response.json()}

    def patch_request(self, url, data, token):
        headers = {'authorization': token}
        response = requests.patch(url=url, data=data, headers=headers)
        return {"status_code": response.status_code, "text": response.json()}

    def get_request(self, url):
        response = requests.get(url=url, data={})
        return {"status_code": response.status_code, "text": response.json()}

    def get_request_with_token(self, url, token):
        headers = {'authorization': token}
        response = requests.get(url=url, data={}, headers=headers)
        return {"status_code": response.status_code, "text": response.json()}