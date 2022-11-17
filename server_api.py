'''
functions responsible for all query interactions with the logion database

authors: Eugene Liu

'''
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Identity, BLOB
from sqlalchemy.orm import declarative_base
from sqlalchemy import insert, select

# uncomment for local
#db_string = "sqlite:////database.db"
db_string = "postgresql://eitohxzsrpboeq:14718d25bf62d075842a7760aa27d4ccc4dae0b61b03cab2d426739a35d42507@ec2-54-174-31-7.compute-1.amazonaws.com:5432/d7nh6ggfp9agvo"
engine = create_engine(db_string, echo=True)
base = declarative_base()

# declaring users table
class User(base):
    __tablename__ = "users"
    
    user_id = Column(String(500), primary_key=True)
    name = Column(String(500))
    email = Column(String(500))
    institution = Column(String(500))
    position = Column(String(500))
    ip_address = Column(String(500))
    
    def __init__(self, user_id, name, email, institution, position, ip_address):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.time = institution
        self.position = position
        self.ip_address = ip_address
        
# declaring texts table
class Text(base):
    __tablename__ = "texts"
    
    text_id = Column(Integer, Identity(start = 1, cycle=True), primary_key=True)
    user_id = Column(String(500))
    text_name = Column(String(8000))
    uploaded = Column(String(8000))
    save_time = Column(String(500))
    
    def __init__(self, text_id, user_id, text_name, uploaded, save_time):
        self.text_id = text_id
        self.user_id = user_id
        self.text_name = text_name
        self.uploaded = uploaded
        self.save_time = save_time

# declaring predictions table
class Prediction(base):
    __tablename__ = "predictions"
    
    prediction_id = Column(Integer, Identity(start = 1, cycle=True), primary_key=True)
    token_number = Column(Integer)
    text_id = Column(Integer)
    prediction_name = Column(String(8000))
    prediction_output = Column(String(8000))
    save_time = Column(String(100))
    prediction_blob = Column(BLOB)
    
    def __init__(self, prediction_id, token_number, text_id, prediction_name, prediction_output, save_time, prediction_blob):
        self.prediction_id = prediction_id
        self.text_id = text_id
        self.token_number = token_number
        self.prediction_name = prediction_name
        self.prediction_output = prediction_output
        self.save_time = save_time
        self.prediction_blob = prediction_blob
        
base.metadata.create_all(engine)
engine.dispose()

def confirm_user(userID:str):
    '''Function that checks if user is in the database'''
    conn = engine.connect()

    stmt = select(User).where(User.user_id == userID)
    result = conn.execute(stmt)
    
    conn.close()
    
    print("we are getting a result")
    if result is None:
        return False
    else:
        return True
    
def add_account(parameter_dict: dict):
    '''Function for adding account information: takes in a dictionary 
        with the following key and value pairs
    '''
    
    # unpacking dictionary items
    ID = parameter_dict.get("id")
    name = parameter_dict.get("name")
    email = parameter_dict.get("email")
    institution = parameter_dict.get("institution")
    position = parameter_dict.get("position")
    ip_address = parameter_dict.get("ip_address")
    

    # adding it to the users table
    stmt = insert(User).values(user_id=ID, name=name, 
                                email=email, 
                                institution=institution, 
                                position=position,
                                ip_address=ip_address)

    # execution of stmt
    conn = engine.connect()
    result = conn.execute(stmt)
    
    # closing connection
    conn.close()
    
def update_account(parameter_to_update: dict, userID: int):
    '''Function that updates user accounts with dictonary of parameters to update using the same
       key/value pairs in the users table and userID of user to be updated.
    '''
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
    
    SQL_str += " WHERE user_id=" + str(userID)
    with engine.connect() as con:
        rs = con.execute(SQL_str)
        con.close()

    
def get_text(userid:str):
    '''
    Function that returns arrays of dicts where each dict is a row of a text query. Each
    row/dict will have the following keys: "textid", "userid", "textname", "uploaded" (text), "save_time". 
    '''
    conn = engine.connect()
    
    # creating SQL statement
    stmt = select(Text).where(Text.user_id == userid)
    result = conn.execute(stmt)
    
    conn.close()
    
    if result is None:
        return None
    
    text_array = []
    for text in result:
        text = list(text)
        text_dict = {}
        
        text_dict["textid"] = text[0]
        text_dict["userid"] = text[1]
        text_dict["textname"] = text[2]
        text_dict["uploaded"] = text[3]
        text_dict["save_time"] = text[4]
        
        text_array.append(text_dict)

    return text_array

def get_predictions(textID: int):
    ''''
    Function that returns arrays of dicts where each dict is a row of prediction query. Each
    row/dict will have the following keys: "textid", "prediction_name", "token_number", 
    "prediction_output" (text), "save_time", "prediction_blob". 
    '''

    conn = engine.connect()
    
    
    # creating SQL statement
    stmt = select(Prediction).where(Prediction.text_id == textID)
    result = conn.execute(stmt)
    
    conn.close()
    
    if result is None:
        return None
    
    prediction_array = []
    for prediction in result:
        prediction = list(prediction)
        prediction_dict = {}
        
        prediction_dict["prediction_id"] = prediction[0]
        prediction_dict["token_number"] = prediction[1]
        prediction_dict["text_id"] = prediction[2]
        prediction_dict["prediction_name"] = prediction[3]
        prediction_dict["prediction_output"] = prediction[4]
        prediction_dict["save_time"] = prediction[5]
        prediction_dict["prediction_blob"]       
        prediction_array.append(prediction_dict)

    return prediction_array

def upload_text(text: str, text_name: str, userid: str, save_time: str):
    '''uploads text'''

    stmt = insert(Text).values(user_id=userid, text_name=text_name,
                                uploaded=text, save_time=save_time)

    # execution of stmt
    conn = engine.connect()
    result = conn.execute(stmt)
    conn.close()
        

def upload_prediction(prediction: str, textid: int, token_number: int, prediction_name: str,
                      save_time:str, prediction_blob: BLOB):
    '''Function that uploads prediction to database'''

    stmt = insert(Prediction).values(token_number=token_number, text_id=textid,
                                      prediction_name=prediction_name,
                                      prediction_output=prediction, 
                                      save_time=save_time,
                                      prediction_blob=prediction_blob)

    
    # execution of stmt
    conn = engine.connect()
    result = conn.execute(stmt)
    conn.close()

def update_text(update_dict: dict, textid):
    '''Updates text by passing in a dictionary of values and columns to modify
       as well as a textid
    '''
    columns = update_dict.keys
    for i, col in enumerate(columns):
        if i == 0:
            SQL_str += col + "=" + update_dict[col]
        else:
            SQL_str += ", " + col + "=" + update_dict[col]
    
    SQL_str += "WHERE textid=" + str(textid)

    with engine.connect() as con:
        rs = con.execute(SQL_str)
        con.close()


def update_prediction(update_dict: dict, predictionid: int):
    '''Updates text by passing in a dictionary of values and columns to modify
       as well as a predictionid
    '''
    SQL_str = "UPDATE predictions SET "
    
    columns = update_dict.keys
    for i, col in enumerate(columns):
        
        if i == 0:
            SQL_str += col + "=" + update_dict[col]
        else:
            SQL_str += ", " + col + "=" + update_dict[col]
    
    SQL_str += "WHERE predictionid=" + str(predictionid)

    with engine.connect() as con:
        rs = con.execute(SQL_str)


    
    



