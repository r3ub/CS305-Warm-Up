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

import re

input_string = "Alabama"

#note: trim whitespace before/after query
def parse_string(userInput):
    if(userInput):
        userInput = userInput.strip()
        keywords = ['state', 'median age', 'obesity rate', 'cow-human ratio', 'life expectancy', 'ski resort']
        symbols = [' > ', ' < ', ' == ']
        valid = False
        tokenizedQuery = userInput.split(' and ')
        for query in tokenizedQuery:
            for keyword in keywords:
                if(query.startswith(keyword)):
                    for symbol in symbols:
                        if(query[len(keyword):].startswith(symbol)):
                            print('valid so far')

def main():
    string = "median age == 5 and state == Alabama and obesity rate > 5"
    parse_string(string)

main()



    


    