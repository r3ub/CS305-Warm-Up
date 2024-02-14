import firebase_connection as fc
from google.cloud.firestore_v1 import FieldFilter

# Firebase Connection Setup
cred, app, store = fc.fb_conn()

#parse_string takes a string of user input and returns a list of queries and keywords based on that input
def parse_string(userInput):
    if(userInput):
        userInput = userInput.lower()
        #states = create_dictionary()
        queries = []
        #used to check whether invalid input msg must be printed
        valid = False
        #trim trailing/leading whitespace
        userInput = userInput.strip()
        #keywords for the start of the query
        keywords = ['state', 'median_age', 'obesity_rate', 'cow_human_ratio', 'life_expectancy', 'ski_resort']
        #valid query symbols
        symbols = [' > ', ' < ', ' == ', ' of ']
        #split on conjunction
        tokenizedQuery = userInput.split(' and ')
        #loops through each
        if(userInput != 'help'):
            for x in range(0, len(tokenizedQuery)):
                for keyword in keywords:
                    if(tokenizedQuery[x].startswith(keyword)):
                        for symbol in symbols:
                            if(tokenizedQuery[x][len(keyword):].startswith(symbol)):
                                value = tokenizedQuery[x][len(keyword) + len(symbol):]
                                if(isDigit(value)):
                                    value = float(value)
                                else:
                                    lst = [word[0].upper() + word[1:] for word in value.split()]
                                    value = " ".join(lst)
                                queries.append((keyword, symbol.strip(), value))
                                valid = True
        else:
            print("Queries are made in the following manner:\n1. Enter a keyword: (state, median_age, obesity_rate, cow_human_ratio, life_expectancy, ski_resort)\n2. Enter a connecting symbol (>, <, or ==). == is used to get the stats of a single state (see example)\n3. Enter a value (either a state name or a double)\n4. Example queries: 'median_age < 40.2', 'obesity_rate > 35 and life_expectancy > 75', 'state == Vermont'\n5. Type 'quit' to quit")
            valid = True
        if(not valid):
            print("Invalid input. Type 'HELP' for assistance")
    return queries

#do_query takes an item, symbol, and value and returns a list of dictionary entries that match the 
#passed arguments (i.e. that fit the criteria of the query)
def do_query(item, symbol, value):
    symbol = symbol.strip()
    return_list = []
    ref = store.collection(u'state-data')
    docs = ref.where(filter=FieldFilter(item, symbol, value)).stream()
    for doc in docs:
        return_list.append(doc.to_dict())
    return return_list

#print_query formats and prints the entries that match the query of the user
def print_query(return_list, item_list):
    for state_info in return_list:
        # First, check if 'state' key exists to avoid KeyError
        state_name = state_info.get('state', "Unknown State")
        # Handle printing based on the item being queried
        state_list = []
        for item in item_list:
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
                len_items = len(item_list)
                # For other items, print state and the item's value
                # Use .get() to safely access item value and provide a default if not found
                if (state_name not in state_list):
                    print(f"State: {state_name}, ", end='')
                    for item in item_list:
                        item_value = state_info.get(item, "Not available")
                        print(f"{item}: {item_value}   ", end='')
                    print("")
                    state_list.append(state_name)

#command_line_interface allows the user to interface with the program with Terminal or another CLI
def command_line_interface():
    user_input = input(
        "\nEnter your query in the format: field_name operator value. Use 'and' for multiple queries. Type 'HELP' for assistance.: ")
    numAnds = getAndCount(user_input)
    #loops through userInput entries and prints output as long as they do not type quit
    while(user_input.lower() != 'quit'):
        queries = parse_string(user_input)
        big_list = []
        final_list = []
        item_list = []
        for query in queries:
            item, symbol, value = query
            results = do_query(item, symbol, value)
            item_list.append(item)
            for entry in results:
                big_list.append(entry)
        for entry in big_list:
            if((big_list.count(entry) == numAnds) and (entry not in final_list)):
                final_list.append(entry)
        # Assuming print_query is intended to print results; this part might need to be adjusted based on actual requirements
        print_query(final_list, item_list)
        user_input = input(
        "Enter your query in the format: field_name operator value. Use 'and' for multiple queries. Type 'HELP' for assistance.: ")


def isDigit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

#counts number of ands and returns that value + 1 (really, it counts the number of queries)
def getAndCount(list_to_split):
    splitList = list_to_split.split(' and ')
    return len(splitList)

def main():
    command_line_interface()

main()