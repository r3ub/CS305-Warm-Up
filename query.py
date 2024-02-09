import firebase_connection as fc
from google.cloud.firestore_v1 import FieldFilter

# Firebase Connection Setup
cred, app, store = fc.fb_conn()


#note: trim whitespace before/after query
def parse_string(userInput):
    if(userInput):
        userInput = userInput.lower()
        #to account for conjunction
        hitslist = []
        #make states dictionary
        #states = create_dictionary()
        queries = []
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
                            if(value.isdigit()):
                                value = float(value)
                            else:
                                value = value.capitalize()
                            #print(do_query(keyword, symbol, value))
                            queries.append((keyword, symbol.strip(), value))
    return queries

def do_query(item, symbol, value):
    symbol = symbol.strip()
    return_list = []
    ref = store.collection(u'state-data')
    docs = ref.where(filter=FieldFilter(item, symbol, value)).stream()
    for doc in docs:
        return_list.append(doc.to_dict())
    return return_list

def print_query(return_list, item):
    for state_info in return_list:
        # First, check if 'state' key exists to avoid KeyError
        state_name = state_info.get('state', "Unknown State")

        # Handle printing based on the item being queried
        if item == 'state':
            if 'state' in state_info:
                print(f"State: {state_info['state']}")
            # Print all key-value pairs except the 'state' to avoid repetition
            for key, value in state_info.items():
                if key == 'state':
                    print("State:", key)
                if key != 'state':  # Skip printing the state name again
                    print(f"{key.capitalize()}: {value}")
        else:
            # For other items, print state and the item's value
            # Use .get() to safely access item value and provide a default if not found
            item_value = state_info.get(item, "Not available")
            print(f"State: {state_name}, {item}: {item_value}")


def command_line_interface():
    user_input = input(
        "Enter your query in the format: field_name operator value, and use 'and' for multiple queries: ")
    queries = parse_string(user_input)
    for query in queries:
        item, symbol, value = query
        results = do_query(item, symbol, value)
        # Assuming print_query is intended to print results; this part might need to be adjusted based on actual requirements
        print_query(results, item)

def main():
    command_line_interface()
    # Create the dictionary and print it to see the structure
    #states_dictionary = create_dictionary()
    # format and print the dictionary to make it readable
    #print(format_dictionary(states_dictionary))


main()

    


    