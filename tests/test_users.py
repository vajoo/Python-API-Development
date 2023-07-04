import sys
import os
  
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
  
sys.path.append(parent_directory)

import pytest
from jose import jwt
from app import schemas
from app.config import settings

def test_create_user(client):
    # fast api is redirecting to '/users/' if you just type '/users' and then it´s possible that the test fails because the status_code is the redirect code 307 and not 201
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "1235"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login/", data={"username": test_user['email'], "password": test_user['password']}) # use data instead of json if you want to send data as form-dat
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("username, password, status_code", [('wrong_email@gmail.com', '12345', 403), ("laurin@gmail.com", 'wrong_password', 403), ('wrong_email@gmail.com', 'wrong_password', 403), (None, '12345', 422), ('laurin@gmail.com', None, 422)])
def test_incorrect_login(client, username, password, status_code):
    res = client.post("/login/", data={"username": username, "password": password})
    assert res.status_code == status_code