# imports 

from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return { "output": "this is the response"}


@app.get("/getCustomer/{customer_id}")
def get_customer(customer_id: int):
    if(customer_id%2 == 0):
        return { "output": "this is a even customer"}
    else: 
        return {
            "output": "this is a odd customer"
        }
    
