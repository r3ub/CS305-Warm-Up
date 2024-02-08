# admin file
# used https://medium.com/@cbrannen/importing-data-into-firestore-using-python-dce2d6d3cd51 as a reference

import json
import firebase_connection as fc

# Firebase Connection Setup
cred, app, store = fc.fb_conn()

# Firebase Collection Setup (Scraps all old data under 'state-data')
doc_ref = store.collection(u'state-data')
store.recursive_delete(doc_ref)

# Load json file
state_json = "state-data.json"
open_j = open(state_json)
state_data = json.load(open_j)

# Iterate through items in json file, add them to Firebase
#   Would normally be worried about batch size, but our dataset is small enough
#   that it won't infringe on Firebase's limits
for state in state_data:
    doc_ref.add(state)
    # Print statement exists just to double-check code (and watch progress)
    print(state)
