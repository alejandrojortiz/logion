'''
functions responsible for all query interactions with the logion database

authors: Eugene Liu

'''
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
    
def add_account(ID: int, name: str, email: str, password: str, institution: str, position: str):
    '''Function for updating account information'''
    
    # making connection with database
    conn = __connect()
    
    # making cursor
    curr = conn.cursor()
    
    # adding user account info into user accounts table
    SQL_str = "INSERT INTO users (userid, name, email, password, institution, position) "
    SQL_str += "VALUES (" + str(ID)
    SQL_str += ", " + name
    SQL_str +=  ", " + email
    SQL_str += ", " + password
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

    curr.execute(SQL_str)
    curr.close()
    conn.close()
    
    print("User account has been successfully updated")

def get_text_options(ID:int):
    '''Function that returns all previously uploaded text in array'''
    
    conn = connect()
    curr = conn.cursor()
    
    return texts

def get_predictions(textID: int):
    '''Function that returns predictions from textID in array'''
    predictions = None
    
    return predictions

def upload_text(text: str, userid: int):
    '''Function that stores user uploaded text to database'''
    pass

def upload_prediction(prediction: str, textid: int):
    '''Function that uploads prediction to database'''

def update_text(text: str, textid:int):
    '''Function that updates an existing uploaded text stored in the database'''
    pass

def update_prediction(prediction: str, textid:int):
    '''Function that updates an existion upload prediction stored in the database'''
    pass

    
    
    
    



