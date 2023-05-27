from fastapi import FastAPI
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# start app with uvicorn: uvicorn <package-name>.<filename>:<fastapi-instance-name> --reload -> uvicorn app.main:app --reload
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# TODO
# - Refresh token mechanism
# - disable user in database mechanism
# - add user role