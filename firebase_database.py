import requests
import json
import re


FIREBASE_DATABASE = "https://fir-db-9cafc-default-rtdb.europe-west1.firebasedatabase.app/"


def valid_reg_ex(regx : str):
	try:
		re.compile(regx)
		return True
	except re.error:
		return False


def read_gr_database(guardrail_id : str):
    try:
        if type(guardrail_id) != str or "." in guardrail_id or "/" in guardrail_id:
            # The latter two conditions prevent access to other parts of the database
            return (400, {}) # Bad request input
        else:
            firebase_url = FIREBASE_DATABASE + f'guardrails/{guardrail_id}.json'
            response = requests.get(firebase_url)

            if response.status_code != 200 or response.json() == None:
                return (404, {}) # ID not found
            else:
                return (200, response.json()) # OK
    except:
        return (500, {}) # Internal server error
    

def list_gr_database():
    try:
        firebase_url = FIREBASE_DATABASE + f'guardrails.json'
        response = requests.get(firebase_url)

        if response.status_code != 200 or response.json() == None:
            return (200, []) # OK - no guardrails in database
        else:
            return (200, list(response.json()))  # OK
    except:
        return (500, []) # Internal server error


def add_gr_database(guardrail_id : str, guardrail_json : dict):
    try:
        properties = {"id", "regx", "sub"}

        if type(guardrail_json) != dict or properties.issubset(guardrail_json) == False:
            # If the guardrail JSON object does not have the three required properties
            return (400, {}) # Bad request input
        elif [type(guardrail_json[prop]) for prop in properties] != [str, str, str]:
            # If the values in the guardrail JSON object are not strings
            return (400, {}) # Bad request input
        elif guardrail_id != guardrail_json["id"] or "." in guardrail_id or "/" in guardrail_id:
            # The latter two conditions prevent access to other parts of the database
            return (400, {}) # Bad request input
        elif valid_reg_ex(guardrail_json["regx"]) == False:
            # If the guardrail regular expression is invalid
            return (400, {})
        else:
            firebase_url = FIREBASE_DATABASE + f'guardrails.json'
            data = {guardrail_id : guardrail_json}
            response = requests.patch(firebase_url, json.dumps(data))

            if response.status_code != 200 or response.json() != data:
                return (404, {}) # Something went wrong
            else:
                return (201, {}) # OK - guardrail added
    except:
        return (500, {})
    

def remove_gr_database(guardrail_id : str):
    try:
        if type(guardrail_id) != str or "." in guardrail_id or "/" in guardrail_id:
            # The latter two conditions prevent access to other parts of the database
            return (400, {}) # Bad request input
        else:
            if read_gr_database(guardrail_id)[0] == 200:
                firebase_url = FIREBASE_DATABASE + f'guardrails/{guardrail_id}.json'
                requests.delete(firebase_url)

                return (204, {}) # OK
            else:
                return (404, {}) # ID not found
                    
    except:
        return (500, {})
    

def clear():
    try:
        firebase_url = FIREBASE_DATABASE + f'guardrails.json'
        requests.delete(firebase_url)
    except Exception as e:
        print(e)
        return None
    
#print(read_gr_database("two"))
#print(remove_gr_database("three"))
#print(add_gr_database("three", {"id" : "three", "regx" : "reggie", "sub" : "sub"}))
#print(list_gr_database())
#print(clear())