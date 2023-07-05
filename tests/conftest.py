import sys
import os
  
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
  
sys.path.append(parent_directory)

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app import models
from app.oauth2 import create_access_token

# 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture() # fixure functions runs before every single function call in of the test_users.py file if the scope is empty or set to function but now it runs one time and closes db conncetion after every test_function was running
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture() # fixure functions runs before every single function call in of the test_users.py file if the scope is empty or set to function but now it runs one time and closes db conncetion after every test_function was running
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app) # yield is likely the same as return but you can run code after it


@pytest.fixture
def test_user(client):
    user_data = {"email": "laurin@gmail.com", "password": "12345"}
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "laurin2@gmail.com", "password": "12345"}
    res = client.post("/users/", json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    post_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user['id']
        },
        {
            "title": "4th title",
            "content": "4th content",
            "owner_id": test_user2['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts