'''
Methods for connecting with flask server

author: Jay White
'''

import flask
import server_api
from google.oauth2 import id_token
from google.auth.transport import requests

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    '''initial index page'''
    html_code = flask.render_template("index.html")
    response = flask.make_response(html_code)
    return response

@app.route('/auth', methods=['POST'])
def auth():
    csrf_token_cookei = flask.request.cookies.get('g_csrf_token')
    if not csrf_token_cookie:
        webapp2.abort(400, 'No CSRF token in Cookie.')
    csrf_token_body = self.request.get('g_csrf_token')
    if not csrf_token_body:
        webapp2.abort(400, 'No CSRF token in post body.')
    if csrf_token_cookie != csrf_token_body:
        webapp2.abort(400, 'Failed to verify double submit cookie.')

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), '492185340356-n66a7tlk0efi4ccds9pbfmo77rs5mjdq.apps.googleusercontent.com')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        username = idinfo['name']
        email = idinfo['email']

        args_dict = {}

        args_dict['username'] = username
        args_dict['email'] = email
        args_dict['userid'] = userid
        args_dict['institution'] = None
        args_dict['postition'] = None

        # if server_api.contains_user(userid):
            # pass
        # else:
            # server_api.add_account(args_dict)


    except ValueError:
        # Invalid token
        pass

@app.route('/account/<userid>', methods=['GET', 'POST'])
def account(userid):
    '''account landing page'''

        # text_array of dicts where each dict is a row of a text query
        # Each row/dict has keys: "textid", "userid", "textname", "uploaded" (text)
        # if server_api.contains_user(userid):
            # text_array = server_api.get_text(userid)
        # else:
        text_array = None
        html_code = flask.render_template("account.html", userid=userid, text_array=text_array)

    response = flask.make_response(html_code)

    return response

#-----------------------------------------------------------------------

def temporary_prediction(text, parameters):
    output = [[['elre', '##lv'], 0.04347], [['erl', '##kpi'], 0.019174], [['erl', '##labe'], 0.0078557]]
    return output

@app.route('/project/<userid>/<textid>', methods=['GET'])
def project(userid, textid):
    '''Page containing main project interface'''

    if textid is "0":
        textname = ""
        uploaded = ""
    
    else:
        textname = text_dict.get("textname")
        uploaded = text_dict.get("uploaded")

    # prediction_array of returns arrays of dicts where each dict is a row of prediction query
    # Each row/dict has keys: "textid", "prediction_name", "token_number", "prediction" (text)
    prediction_array = get_predictions(textID=textid)

    # parameters = {}
    # token_number = flask.request.args.get('token-number')
    # paramters["token_number"] = token_number

    # if text_masked is not None:
        # prediction = temporary_prediction(uploaded, parameters)

    html_code = flask.render_template("project.html", text_name=textname, uploaded=uploaded
                                       prediction_array=prediction_array)
    response = flask.make_response(html_code)

    return response

@app.route('/predict/<text>', methods=[POST])
def predict(text):
    pass