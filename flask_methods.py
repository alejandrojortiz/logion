'''
Methods for connecting with flask server

author: Jay White
'''

import flask
import server_api

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


@app.route('/account/<userid>', methods=['GET', 'POST'])
def account(userid):
    '''account landing page'''
    if request.method == 'POST':
        # create account
        username = flask.request.args.get('username')
        email = flask.request.args.get('email')
        institution = flask.request.args.get('institution')
        userid = flask.request.args.get('userid')

        args_dict = {}

        if username is not None:
            args_dict['username'] = username
        if email is not None:
            args_dict['email'] = email
        if institution is not None:
            args_dict['institution'] = institution
        if userid is not None:
            args_dict['userid'] = userid

        server_api.add_account(args_dict)

        html_code = flask.render_template("account.html", userid=userid, text_array=None)

    else:
        # existing account
        userid = flask.request.args.get('userid')

        # text_array of dicts where each dict is a row of a text query
        # Each row/dict has keys: "textid", "userid", "textname", "uploaded" (text)
        text_array = server_api.get_text(userid)
        html_code = flask.render_template("account.html", userid=userid, text_array=text_array)

    response = flask.make_response(html_code)

    return response

#-----------------------------------------------------------------------

def temporary_prediction(text, parameters):
    output = [[['elre', '##lv'], 0.04347], [['erl', '##kpi'], 0.019174], [['erl', '##labe'], 0.0078557]]
    return output

@app.route('/project/<userid>/<textid>', methods=['GET'])
def project(userid, textid, text_dict, prediction_array, text_masked, prediction):
    '''Page containing main project interface'''

    textname = text_dict.get("textname")
    uploaded = text_dict.get("uploaded")

    # prediction_array of returns arrays of dicts where each dict is a row of prediction query
    # Each row/dict has keys: "textid", "prediction_name", "token_number", "prediction" (text)
    prediction_array = get_predictions(textID=textid)

    parameters = {}
    token_number = flask.request.args.get('token-number')
    paramters["token_number"] = token_number

    if text_masked is not None:
        prediction = temporary_prediction(uploaded, parameters)

    html_code = flask.render_template("project.html", userid=userid, textid=textid, 
                                      text_dict=text_dict, prediction_array=prediction_array,
                                      text_masked=text_masked, prediction=prediction)
    response = flask.make_response(html_code)

    return response