import firebase_admin, os
from firebase_admin import credentials, storage, firestore
from spreadsheet import update_sheet

cred = credentials.Certificate("credentials.json")
fire_app = firebase_admin.initialize_app(cred)

firebaseConfig = {
  "apiKey": "AIzaSyBj3HivDta8E8HN0FYQJetBx7JCffS2pGE",
  "authDomain": "kumuweb-dae5e.firebaseapp.com",
  "projectId": "kumuweb-dae5e",
  "storageBucket": "kumuweb-dae5e.appspot.com",
  "messagingSenderId": "42512105158",
  "appId": "1:42512105158:web:7c013eb6de9583c20e21c7",
  "measurementId": "G-PL6D41DH8K"
}

db = firestore.client()

# EACH ROW IS ONE DOCUMENT
    # - In Elements, the name of each document is the Label cell
    # - In Connections, the name of each document is the From cell

def find_ref(collection, document):
    return db.collection(collection).document(document)

def num_docs(collection):

    collection_ref = db.collection(collection)

    docs = collection_ref.stream()
    
    doc_count = sum(1 for _ in docs)
    
    return doc_count

# Creates an Element label.
def create_element(description, label, tags, type):
    # Check which collection it should be first.
        # - For now it is just assumed to be the Elements collection.

    try:
        result = db.collection("Elements").document(label).set(
            {
                "Description": description,
                "Label": label,
                "Tags": tags,
                "Type": type
            }
        )

        # And then with the values array, it calls the other function to actually associate the values of "TO" and "FROM" with each other.            

        return {"status": f"Success: {result}"}
    except Exception as e:
        return {"status": f"Failure: {e}"}
    
def link_docs(from_el, to_els):
    # When a new Connection is formed, it should check against the current Elements to see if those Elements exit.
        # - If they exist, then carry on as usual.
        # - If they don't exist, then CREATE them.

    from_el_ref = ""
    to_els_refs = []

    # Finds the reference to the correct elements:
    try:
        # From Element reference:
        from_el_ref = find_ref("Elements", from_el)

        # To Elements references:
        for el in to_els:
            to_els_refs.append(find_ref("Elements", el))
    except Exception as e:
        return {"status": f"Failed to find from_el: {e}"}

    try:
        result = db.collection("Connections").document(from_el).set(
            {
                "From": from_el_ref,
                "To": to_els_refs
            }
        )
        return {"status": "Successfully linked docs"}
    except Exception as e:
        return {"status": f"Failure to link_docs: {e}"}