import re

import json
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Connection Setup
cred = credentials.Certificate("firebase-adminsdk-key.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()

# Firebase Collection Setup (Scraps all old data under 'state-data')
doc_ref = store.collection(u'state-data')
store.recursive_delete(doc_ref)

#Query Language:
# INPUT                     RETURN  
# state == X                all stats for state X
# median age X              median age for state X
# median age >/< X          all states with median age over/under X
# obesity rate X            obesity rate for state X
# obesity rate >/< X        all states with obesity rate over/under X 
# cow-human ratio X         cow-human ratio for state X
# cow-human ratio >/< X     all states with cow-human ratio over/under X
# life expectancy X         life expectancy for state X
# life expectancy >/< X     all states with life expectancy over/under X
# ski resort X              T/F if a ski resort exists in state X. If true, number of ski resorts
# functionality for and

#note: trim whitespace before/after query
def parse_string(userInput):
    if(userInput):
        #make states dictionary
        states = create_dictionary()
        #trim trailing/leading whitespace
        userInput = userInput.strip()
        #keywords for the start of the query
        keywords = ['state', 'median_age', 'obesity_rate', 'cow_human_ratio', 'life_expectancy', 'ski_resort']
        #valid query symbols
        symbols = [' > ', ' < ', ' == ', ' of ']
        valid = False
        #split on conjunction
        tokenizedQuery = userInput.split(' and ')
        #loops through each 
        for x in range(0, len(tokenizedQuery)):
            for keyword in keywords:
                if(tokenizedQuery[x].startswith(keyword)):
                    for symbol in symbols:
                        if(tokenizedQuery[x][len(keyword):].startswith(symbol)):
                            value = tokenizedQuery[x][len(keyword) + len(symbol):]
                            if(symbol == ' of ' or (keyword == 'state' and symbol == ' == ')):
                                if(value in states):
                                    do_state_query(value)
                            elif(value.replace('.', '', 1).isdigit()):
                                do_attribute_query(keyword, symbol, value)

def create_dictionary():
    # Load json file
    state_json = "state-data.json"
    open_j = open(state_json)
    state_data = json.load(open_j)
    # Initialize an empty dictionary to hold the states and their data
    states_dict = {}

    # Iterate over each state's data in the list
    for state_info in state_data:
        # Use the state's name as the key, and the remaining data as the value
        state_name = state_info['state']
        # Remove the state name from the data to avoid redundancy
        del state_info['state']
        # Assign the modified dictionary as the value for the state key
        states_dict[state_name] = state_info

    return states_dict

def format_dictionary(states_dict):
    for state, data in states_dict.items():
        print(f"State: {state}")
        for key, value in data.items():
            print(f"  {key.replace('_', ' ').capitalize()}: {value}")
        print()

def do_state_query(value):
    states = create_dictionary()
    for state in states:
        if(state == value):
            print(states.get(state))

def do_attribute_query(keyword, symbol, value):
    states = create_dictionary().items()
    for item in states:
        if(symbol == ' > '):
            if(item[1].get(keyword) > float(value)):
                print(item)
        elif(symbol == ' < '):
            if(item[1].get(keyword) < float(value)):
                print(item)
        else:
            if(item[1].get(keyword) == float(value)):
                print(item)

def main():
    string = "median_age > 43 and state == Alabama and obesity_rate > 40 and obesity_rate of Texas"
    parse_string(string)
    # Create the dictionary and print it to see the structure
    states_dictionary = create_dictionary()
    # format and print the dictionary to make it readable
    #print(format_dictionary(states_dictionary))

main()

    


    