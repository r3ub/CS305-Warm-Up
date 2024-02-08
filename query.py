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
        #trim trailing/leading whitespace
        userInput = userInput.strip()
        #keywords for the start of the query
        keywords = ['state', 'median age', 'obesity rate', 'cow-human ratio', 'life expectancy', 'ski resort']
        #valid query symbols
        symbols = [' > ', ' < ', ' == ', ' of ']
        valid = False
        #split on conjunction
        tokenizedQuery = userInput.split(' and ')
        #loops through each 
        for query in tokenizedQuery:
            for keyword in keywords:
                if(query.startswith(keyword)):
                    for symbol in symbols:
                        if(query[len(keyword):].startswith(symbol)):
                            print('valid so far')

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

def main():
    string = "median age == 5 and state == Alabama and obesity rate > 5 and obesity rate of Texas"
    parse_string(string)
    # Create the dictionary and print it to see the structure
    states_dictionary = create_dictionary()
    # format and print the dictionary to make it readable
    print(format_dictionary(states_dictionary))

main()

    


    