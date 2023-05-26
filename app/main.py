from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)

# start app with uvicorn: uvicorn <package-name>.<filename>:<fastapi-instance-name> --reload -> uvicorn app.main:app --reload
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# TODO
# - Refresh token mechanism
# - disable user in database mechanism
# - add user role