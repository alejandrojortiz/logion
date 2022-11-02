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
        

@app.route('/account/<sub>', methods=['GET', 'POST'])
def account(sub):
    '''account landing page'''
    if request.method == 'POST':
        # create account
        name = flask.request.args.get('name')
        email = flask.request.args.get('email')
        institution = flask.request.args.get('institution')
        sub = flask.request.args.get('sub')

        args_dict = {}

        if name is not None:
            args_dict['name'] = name
        if email is not None:
            args_dict['email'] = email
        if institution is not None:
            args_dict['institution'] = institution
        if sub is not None:
            args_dict['sub'] = sub
        
        server_api.add_account(args_dict)

        html_code = flask.render_template("account.html", sub=sub, user_name=user_name
                                          projects=None)

    else:
        # existing account
        sub = flask.request.args.get('sub')
        user_name, projects = server_api.login(sub)
        html_code = flask.render_template("account.html", sub=sub, user_name=user_name
                                          projects=projects)

    response = flask.make_response(html_code)

    if sub is not None:
        response.set_cookie("sub", sub)
    
    return response

#-----------------------------------------------------------------------

def temporary_prediction(text, number):
    pass
    

@app.route('/project/<sub>/<proj_id>', methods=['GET'])
def project(sub, proj_id):
    '''Page containing main project interface'''
    if sub is flask.request.cookies.get('sub')
        '''error'''
        pass

    html_code = flask.render_template("project.html", sub=sub, proj_id=proj_id)
    response = flask.make_response(html_code)



    return response