from app import schemas
import pytest 
from app.config import settings
from jose import JWTError, jwt



def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert "First fastAPI running successfully, what's inside container, okay" == res.json().get('message')
    assert res.status_code == 200

# While testing from Postman, we have used the path "/users" and not "/users/" but while testing in this file
# we have used the path "/users/" and if we use just "/users", it is failing, but why?
# because, when we send a request to path "/users", it will be redirected to path "/users/" and the response
# code will be '307', which will not match with '201' and the test fails
def test_create_users(client):
    res = client.post("/users/", json={"email": "abcdefg@gmail.com", "password": "password123", "phone_number": 99})
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "abcdefg@gmail.com"
    assert res.status_code == 201

def test_user_login(test_user, client):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password'], "phone_number": 99})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms = [settings.algorithm])
    id: str = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, phone_number, status_code", [
    ('abcdef@gmail.com', 'password123', 99, 403),
    ('abcdefg@gmail.com', 'password1234', 99, 403),
    ('abcdef@gmail.com', 'password1234', 99, 403),
    (None, 'password123', 99, 422),
    ('abcdefg@gmail.com', None, 99, 422)
])
def test_incorrect_login(test_user, client, email, password, phone_number, status_code):
    res = client.post("/login", data={"username": email, "password": password, "phone_number": phone_number})
    assert res.status_code == status_code