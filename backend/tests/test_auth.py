def test_registration(client):

    response = client.post(
        "/auth/register",
        json={
            "full_name": "John Doe",
            "email": "john@test.com",
            "password": "password123",
            "role": "participant"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["full_name"] == "John Doe"
    assert data["email"] == "john@test.com"
    assert data["role"] == "participant"


def test_login(client):

    client.post(
        "/auth/register",
        json={
            "full_name": "Login User",
            "email": "login@test.com",
            "password": "password123",
            "role": "participant"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "login@test.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_login(client):

    client.post(
        "/auth/register",
        json={
            "full_name": "Invalid User",
            "email": "invalid@test.com",
            "password": "password123",
            "role": "participant"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "invalid@test.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401