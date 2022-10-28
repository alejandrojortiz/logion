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
@app.route('/connect', methods=['GET'])
def connect():
    conn = server_api.connect()


@app.route('/add_account', methods=['GET'])
def add_account():
    '''Function that sends user account details to postGRE server'''
    
    # retrieving arguments from html
    name = flask.request.args.get('name')
    email = flask.request.args.get('email')
    password = flask.request.args.get('password')
    institution = flask.request.args.get('institution')
    position = flask.request.args.get('position')
    
    server_api.add_account(name, email, password, institution, position)


#-----------------------------------------------------------------------

@app.route('/update_account', methods=['GET'])
def update_account():
    '''Function that updates user account details to postGRE server'''
    
    # retrieve arguments
    name = flask.request.args.get('name')
    email = flask.request.args.get('email')
    password = flask.request.args.get('password')
    institution = flask.request.args.get('institution')
    position = flask.request.args.get('position')

    # make dictionary and assign args

    args_dict = {}

    if (name == None):
        args_dict['name'] = name
    if (email == None):
        args_dict['email'] = email
    if (password == None):
        args_dict['password'] = password
    if (institution == None):
        args_dict['institution'] = institution
    if (position == None):
        args_dict['position'] = position
    
    server_api.update_account(args_dict)
