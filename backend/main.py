from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from spreadsheet import get_vals, update_sheet
import google.auth
from typing import List
from pydantic import BaseModel
from model import db, create_element, num_docs, link_docs

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"data": "rehaan"}

@app.get("/getvals/{collection}")
async def get_values(collection: str):
    return get_vals(collection)

# Length of values list can be as many, as long as values[0] is always the "FROM" element, it can have as many "TO" elements as it wants
# Row should always be the last row (updates to (row + 1)).
    # Maybe update later, in the UI (SvelteKitJS) or spreadsheet.py file, for convenience, etc.
# If updating "TO" element, update columnIndex to 1.

class Values(BaseModel):
    vals: List[str]
    row: int
    col_ind: int

@app.post("/linkdocs/")
async def link_connections(values: Values):
    print(f"50 - {values}")
    doc_count = num_docs("Connections")
    values.row = doc_count + 1
    try:
        # SHOULD FIRST UPDATE THE FIREBASE DATABASE, AND THEN THE UPDATE_VALUES FUNCTION CAN JUST UPDATE THE SPREADSHEET RELATIVE TO THE CHANGES THAT ARE FOUND IN THE DATABASE.
            # - But the question remains -> What is the best way to store the data?
            # - Two collections:
                # - Elements & Connections (Each are their own sheet name in the Google Sheet as well).
                    # - Database docs: https://blog.kumu.io/the-ultimate-guide-to-using-google-sheets-with-kumu-d46e96fd47a8
                    # - Elements:
                        # - Label, Type, Description
                    # - There should be a separate collection for Tags, as these will probably be getting updated more frequently than the others, and are not specific to single Elements.
                        # - For now I am just using a string specific to each Element. -> Will have to fix this later, etc.

        from_el = ""
        rest_vals = []
        if values.col_ind == 0:
            from_el = values.vals[0]
            rest_vals = values.vals[1::]
        
        try:
            result = link_docs(from_el, rest_vals)
        except Exception as e:
            return {"status": f"Failure to link_docs {e}"}
        update_sheet(os.environ.get("CONNECTIONS_ID"), values.vals, values.row, values.col_ind)
        return {"status": "Success"}
    except Exception as e:
        return {"status": f"Failure to /updatevals/: {e}"}
    
class Label(BaseModel):
    description: str
    label: str
    tags: List[str]
    type: str

@app.post("/createlabel/")
async def update_model(label: Label):
    try:
        print(f"75 - {label}")
        result = create_element(label.description, label.label, label.tags, label.type)

        values = []
        # Adding in the order in which they appear in the spreadsheet:
        values.append(label.label)
        values.append(label.type)
        tags = ", ".join(label.tags) # Moves the list into a single string -> lists can't be processed into one cell through the API.
        values.append(tags)
        values.append(label.description)
        print(f"83 - {values}")
        doc_count = num_docs("Elements")
        row = doc_count
        print(f"Num docs: {doc_count}")
        result = update_sheet(os.environ.get("ELEMENTS_ID"), values,row, 0)
        return {"status": f"Success: {result}"}
    except Exception as e:
        return {f"Failed to create model: {e}"}
