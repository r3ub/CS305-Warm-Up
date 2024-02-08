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
                            print(do_query(keyword, symbol, value))


def do_query(item, symbol, value):
    symbol = symbol.strip()
    return_list = []
    ref = store.collection(u'state-data')
    docs = ref.where(filter=FieldFilter(item, symbol, value)).stream()
    for doc in docs:
        return_list.append(doc.to_dict())
    return return_list

def main():
    string = input('?? ')
    while(string.lower() != 'quit'):
        parse_string(string)
        string = input('??')

main()

    


    