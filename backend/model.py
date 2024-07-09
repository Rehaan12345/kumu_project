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