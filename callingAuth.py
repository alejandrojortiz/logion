'''
Sample authorization credentials
'''
# import urllib

import google.auth.transport.requests
from google.oauth2 import id_token
from google.oauth2 import service_account
import requests as req
from google.auth.transport import requests
import google.oauth2.credentials
from google.auth.transport.requests import AuthorizedSession

def make_authorized_get_request(endpoint, audience):
    """
    make_authorized_get_request makes a GET request to the specified HTTP endpoint
    by authenticating with the ID token obtained from the google-auth client library
    using the specified audience value.
    """
    SERVICE_ACCOUNT_FILE = 'service.json'

    # Cloud Functions uses your function's URL as the `audience` value
    # audience = "https://classics-prediction-auth-xkmqmbb5uq-uc.a.run.app/"
    endpoint = "https://classics-prediction-auth-xkmqmbb5uq-uc.a.run.app/"

    credentials = service_account.IDTokenCredentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, target_audience=endpoint)

    authed_session = AuthorizedSession(credentials)
    authed_session.get(endpoint)
    google.auth.transport.requests.Request()
    token = credentials.token
    # print (token)
    # print(id_token.verify_token(token,request))

    # For Cloud Functions, `endpoint` and `audience` should be equal

    # req = urllib.request.Request(endpoint)

    # auth_req = google.auth.transport.requests.Request()
    # id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)

    # req.add_header("Authorization", f"Bearer {credentials}")
    # print(credentials)
    header = {
        "Authorization": f"Bearer {token}"
        }
    temp = req.post('https://classics-prediction-auth-xkmqmbb5uq-uc.a.run.app/', headers = header)

    return temp

if __name__ == '__main__':
    test = make_authorized_get_request("0", "0")
    print(test)
