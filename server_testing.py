'''
functions responsible for testing server_api

author: Jay White

'''

import server_api
import json

def main():
    """Main method"""
    parameter_dict = {}

    user_id = 13244444
    parameter_dict["user_id"] = user_id
    parameter_dict["name"] = 'Testing12345'
    parameter_dict["email"] = '1902i1@123.com'
    parameter_dict["institution"] = 'University of the southeastwestnorth'
    parameter_dict["position"] = 'God emperor'
    parameter_dict["ip_address"] = json.dumps(parameter_dict).encode('utf-8')

    server_api.add_account(parameter_dict)

    user_dict = server_api.get_user(user_id)

    assert user_dict["user_id"] == parameter_dict["user_id"]
    assert user_dict["name"] == parameter_dict["name"]
    assert user_dict["email"] == parameter_dict["email"]
    assert user_dict["institution"] == parameter_dict["institution"]
    assert user_dict["position"] == parameter_dict["position"]
    assert user_dict["ip_address"] == parameter_dict["ip_address"]

    assert server_api.confirm_user(user_id)

    server_api.update_account(parameter_dict)

    user_dict = server_api.get_user(user_id)

    assert user_dict["user_id"] == parameter_dict["user_id"]
    assert user_dict["name"] == parameter_dict["name"]
    assert user_dict["email"] == parameter_dict["email"]
    assert user_dict["institution"] == parameter_dict["institution"]
    assert user_dict["position"] == parameter_dict["position"]
    assert user_dict["ip_address"] == parameter_dict["ip_address"]

    text = 'Ὡς δὲ καὶ τὴν ἐμὴν πρὸς σὲ φιλίαν τούτοις ἐγνώρισα, πρὸς δὲ καὶ ὅτι με διὰ πάσης ἔχεις αἰδοῦς, γονυπετεῖς αὖθίς μοι γεγονότες, πολλά μου κατεδεήθησαν δι´ ἐμοῦ μεσίτου,'
    text_name = 'Psellos Epistle'
    save_time = '11:11:11 am'

    server_api.upload_text(text=text, text_name=text_name, user_id=user_id, save_time=save_time)

    assert server_api.confirm_text(text_name, user_id)

    text_id = server_api.get_text_id(user_id=user_id, text_name=text_name)

    texts = server_api.get_text(user_id)

    assert texts[0]["text_id"] == text_id
    assert texts[0]["user_id"] == user_id
    assert texts[0]["text_name"] == text_name
    assert texts[0]["uploaded"] == text
    assert texts[0]["save_time"] == save_time

    text_dict = {}

    text_dict['text'] = text
    text_dict['text_name'] = text_name
    text_dict['save_time'] = save_time

    server_api.update_text(text_dict)

    texts = server_api.get_text(user_id)

    assert texts[0]["text_id"] == text_id
    assert texts[0]["user_id"] == user_id
    assert texts[0]["text_name"] == text_name
    assert texts[0]["uploaded"] == text
    assert texts[0]["save_time"] == save_time

    prediction = 'πρὸς'
    token_number = 2
    prediction_name = 'line 3'
    prediction_blob = json.dumps(texts).encode('utf-8')

    server_api.upload_prediction(prediction=prediction, text_id=text_id, token_number=token_number, 
                                prediction_name=prediction_name, save_time=save_time, prediction_blob=prediction_blob)
    
    assert server_api.confirm_prediction(prediction_name=prediction_name, text_id=text_id)

    predictions = server_api.get_predictions(text_id=text_id)

    prediction_id = predictions[0]["prediction_id"]

    assert predictions[0]["prediction_id"] == prediction_id
    assert predictions[0]["text_id"] == text_id
    assert predictions[0]["token_number"] == token_number
    assert predictions[0]["prediction_name"] == prediction_name
    assert predictions[0]["prediction_output"] == prediction
    assert predictions[0]["save_time"] == save_time
    assert predictions[0]["prediction_blob"] == prediction_blob

    server_api.delete_prediction(prediction_name=prediction_name, text_id=text_id)

    server_api.delete_text(text_id=text_id)

if __name__ == "__main__":
    main()