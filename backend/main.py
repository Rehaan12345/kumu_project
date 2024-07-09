from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from spreadsheet import get_values, update_values
import google.auth
from typing import List
from pydantic import BaseModel

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

@app.get("/getvals")
async def get_vals():
    return get_values()

# Length of values list can be as many, as long as values[0] is always the "FROM" element, it can have as many "TO" elements as it wants
# Row should always be the last row (updates to (row - 1)).
    # Maybe update later, in the UI (SvelteKitJS) or spreadsheet.py file, for convenience, etc.
# If updating "TO" element, update columnIndex to 1.

class Values(BaseModel):
    vals: List[str]
    row: int
    col_ind: int

@app.post("/updatevals/")
async def update_vals(values: Values):
    print(values)
    try:
        update_values(values.vals, values.row, values.col_ind)
        return {"status": "Success"}
    except Exception as e:
        return {"status": f"Failure to /updatevals/: {e}"} 