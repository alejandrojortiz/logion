'''
Methods for connecting with flask server

author: Jay White
'''

import flask
import server_api

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='.')

#-----------------------------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    '''initial index page'''
    if request.method == 'POST':
        # create account
        
        name = flask.request.args.get('name')
        email = flask.request.args.get('email')
        institution = flask.request.args.get('institution')
        sub = flask.request.args.get('sub')


        args_dict = {}

        if (name is not None):
            args_dict['name'] = name
        if (email is not None):
            args_dict['email'] = email
        if (institution is not None):
            args_dict['institution'] = institution
        if (sub is not None):
            args_dict['sub'] = sub
        
        server_api.add_account(args_dict)

    else:
        sub = flask.request.args.get('sub')
        user_name, projects = server_api.login(sub)
    
    html_code = flask.render_template("index.html")
    response = flask.make_response(html_code)
    return response
        

@app.route('/account', methods=['GET'])
def account():
    '''account landing page'''


#-----------------------------------------------------------------------

@app.route('/project', methods=['GET'])
def project():
    '''Page containing main project interface'''
    pass
