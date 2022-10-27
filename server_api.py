'''
functions responsible for all query interactions with the logion database

authors: Eugene Liu

'''
import psycopg2
from config import config

def connect():
    '''Function that connects to postgresql server and returns connection object'''
    try:
        
        # getting connection parameters
        params = config()
        
        print("Connection to PostgreSQL database...")
        conn = psycopg2.connect(**params)
        print("Connection established!")
        
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
def add_account(name: str, email: str, password: str, institution: str, position: str):
    '''Function for updating account information'''
    
    # making connection with database
    conn = connect()
    
    # making cursor
    curr = conn.cursor()
    
    # adding user account info into user accounts table
    SQL_str = "INSERT INTO users (name, email, password, institution, position) "
    SQL_str += "VALUES (" + name
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

def update_account(parameter_to_update: dict):
    '''Function for updating account'''
    
    pass



