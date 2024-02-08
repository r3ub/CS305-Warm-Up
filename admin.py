# admin file
# used https://medium.com/@cbrannen/importing-data-into-firestore-using-python-dce2d6d3cd51 as a reference

import json
import sys
import firebase_connection as fc


def firebase_setup():
    # Firebase Connection Setup
    cred, app, store = fc.fb_conn()

    # Firebase Collection Setup (Scraps all old data under 'state-data')
    doc_ref = store.collection(u'state-data')
    store.recursive_delete(doc_ref)

    # Use sys.argv to get the json file, it will be arg 1 (0 is script name)
    state_json = sys.argv[1]

    # Load json file, please use state-data.json with NO QUOTES AROUND IT
    open_j = open(str(state_json))
    state_data = json.load(open_j)

    # Iterate through items in json file, add them to Firebase
    #   Would normally be worried about batch size, but our dataset is small enough
    #   that it won't infringe on Firebase's limits
    for state in state_data:
        doc_ref.add(state)
        # Print statement exists just to double-check code (and watch progress)
        print("\nState:", state)


firebase_setup()