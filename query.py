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
        if(userInput != 'help'): 
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
                                valid = True
                                print(do_query(keyword, symbol, value))
            if(not valid):
                print('Invalid input')
        else:
            print("Queries are made in the following manner:\n1. Enter a keyword: (state, median_age, obesity_rate, cow_human_ratio, life_expectancy, ski_resort)\n2. Enter a connecting symbol (>, <, or ==). == is used to get the stats of a single state (see example)\n3. Enter a value (either a state name or a double)\n4. Example queries: 'median_age < 40.2', 'obesity_rate > 35', state == Vermont'")


def do_query(item, symbol, value):
    symbol = symbol.strip()
    return_list = []
    ref = store.collection(u'state-data')
    docs = ref.where(filter=FieldFilter(item, symbol, value)).stream()
    for doc in docs:
        return_list.append(doc.to_dict())
    return return_list

def main():
    string = input('Enter a query, or type HELP for a list of commands: ')
    while(string.lower() != 'quit'):
        parse_string(string)
        string = input('Enter a query, or type HELP for a list of commands: ')

main()

    


    