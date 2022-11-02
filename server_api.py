'''
functions responsible for all query interactions with the logion database

authors: Eugene Liu

'''
from distutils.log import error
import psycopg2
from config import config

def __connect():
    '''private function that connects to postgresql server and returns connection object'''
    try:
        
        # getting connection parameters
        params = config()
        
        print("Connection to PostgreSQL database...")
        conn = psycopg2.connect(**params)
        print("Connection established!")
        
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
def add_account(parameter_dict: dict):
    '''Function for updating account information'''
    
    # unpacking dictionary items
    ID = parameter_dict.get("id")
    name = parameter_dict.get("name")
    email = parameter_dict.get("email")
    institution = parameter_dict.get("institution")
    position = parameter_dict.get("position")
    
    SQL_str = "INSERT INTO users (id, name, email, institution, position) "
    SQL_str += "VALUES (" + ID + ", "
    SQL_str += email + ", "
    SQL_str += institution + ", "
    SQL_str += position + ");"
    
    # making connection with database
    conn = __connect()
    
    # making cursor
    curr = conn.cursor()
    
    # adding user account info into user accounts table
    
    
    SQL_str = "INSERT INTO users (userid, name, email, institution, position) "
    SQL_str += "VALUES (" + str(ID)
    SQL_str += ", " + name
    SQL_str +=  ", " + email
    #SQL_str += ", " + password
    SQL_str += ", " + institution
    SQL_str += ", " + position
    SQL_str += ");"
    
    # executing statement
    curr.execute(SQL_str)
    
    # closing cursor and database connection
    curr.close()
    conn.close()
    
    print("User added successfully")

def update_account(parameter_to_update: dict, userID: int):
    '''Function for updating account'''
    
    # making connection with database
    conn = __connect()
    curr = conn.cursor()
    
    # getting all parameters to be updated
    parameters = parameter_to_update.keys
    
    # defining base case SQL statement
    SQL_str = "UPDATE users SET "
    
    # adding addition expressions to update
    for i, parameter in enumerate(parameters):
        
        # first case does not need to add comma in the beginning
        if i == 0:
            SQL_str += parameter + "=" + str(parameter_to_update.get(parameter))
        
        else:
            SQL_str += ", " + parameter + "=" + str(parameter_to_update.get(parameter))
    
    SQL_str += ";"
    curr.execute(SQL_str)
    curr.close()
    conn.close()
    
    print("User account has been successfully updated")

def get_text(userid:int):
    '''
    Function that returns arrays of dicts where each dict is a row of a text query. Each
    row/dict will have the following keys: "textid", "userid", "textname", "uploaded" (text). 
    '''
    texts = None
    
    # creating SQL statement
    SQL_str = "SELECT * FROM texts WHERE userid LIKE=" + str(userid) + ";"
    
    try:
        # creating connection to database
        conn = __connect()
        curr = conn.cursor()

        # executing cursor 
        curr.execute(SQL_str)
        texts = curr.fetchall()
        
        text_array = []
        for text in texts:
            text_dict = {}
            text_dict["textid"] = text[2]
            text_dict["userid"] = text[0]
            text_dict["textname"] = text[3]
            text_dict["uploaded"] = text[1]
            
            text_array.append(text_dict)

        curr.close()
        conn.close()
        
    except (Exception, psycopg2.DatabaseError):
        print(error)
    return text_array

def get_predictions(textID: int):
    ''''
    Function that returns arrays of dicts where each dict is a row of prediction query. Each
    row/dict will have the following keys: "textid", "prediction_name", "token_number", 
    "prediction" (text). 
    '''
    predictions = None
    
    # creating SQL statement
    SQL_str = "SELECT * FROM predictions WHERE textid LIKE=" + str(textID) + ";"
    
    try:
        # creating connection to database
        conn = __connect()
        curr = conn.cursor()

        # executing cursor 
        curr.execute(SQL_str)
        predictions = curr.fetchall()
        
        prediction_array = []
        for prediction in predictions:
            prediction_dict = {}
            prediction_dict["textid"] = prediction[0]
            prediction_dict["prediction_name"] = prediction[3]
            prediction_dict["token_number"] = prediction[2]
            prediction_dict["prediction"] = prediction[1]
            prediction_dict["predictionid"] = prediction[4]
            
            prediction_array.append(prediction_dict)

        curr.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError):
        print(error)
    
    return prediction_array

def upload_text(text: str, text_name: str, userid: int):
    '''uploads text'''

    SQL_str = "INSERT INTO texts (useerid, uploaded, textname)"
    SQL_str += "VALUES (" + str(userid) + ", " + text + ", " + text_name + ");"
    
    try:
        # creating connection to database
        conn = __connect()
        curr = conn.cursor()

        # executing upload statement
        curr.execute(SQL_str)

        curr.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError):
        print(error)
        

def upload_prediction(prediction: str, textid: int, token_number: int, prediction_name: str):
    '''Function that uploads prediction to database'''
    
    SQL_str = "INSERT INTO predictions (textid, predictionoutput, tokennumber, predictionname)"
    SQL_str += "VALUES (" + str(textid) + ", " + prediction + ", " + token_number + ", " + str(prediction_name) + ");"

    try:
        # creating connection to database
        conn = __connect()
        curr = conn.cursor()

        # executing upload statement
        curr.execute(SQL_str)

        curr.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError):
        print(error)
        
def update_text(update_dict: dict, textid):
    '''Function that updates an existing uploaded text stored in the database'''
    SQL_str = "UPDATE texts SET "
    
    columns = update_dict.keys
    for i, col in enumerate(columns):
        
        if i == 0:
            SQL_str += col + "=" + update_dict[col]
        else:
            SQL_str += ", " + col + "=" + update_dict[col]
    
    SQL_str += "WHERE textid=" + str(textid) + ";"

    try:
        # creating connection to database
        conn = __connect()
        curr = conn.cursor()

        # executing upload statement
        curr.execute(SQL_str)

        curr.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError):
        print(error)

def update_prediction(update_dict: dict, predictionid: int):
    '''Function that updates an existion upload prediction stored in the database'''
    SQL_str = "UPDATE predictions SET "
    
    columns = update_dict.keys
    for i, col in enumerate(columns):
        
        if i == 0:
            SQL_str += col + "=" + update_dict[col]
        else:
            SQL_str += ", " + col + "=" + update_dict[col]
    
    SQL_str += "WHERE predictionid=" + str(predictionid) + ";"


    try:
        # creating connection to database
        conn = __connect()
        curr = conn.cursor()

        # executing upload statement
        curr.execute(SQL_str)

        curr.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError):
        print(error)
    
    
    



