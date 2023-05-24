from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

# start app with uvicorn: uvicorn <package-name>.<filename>:<fastapi-instance-name> --reload -> uvicorn app.main:app --reload
app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user="postgres", password="postgres", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)
        time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}