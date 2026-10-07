def create_workshop(
    client,
    admin_token,
    capacity=10
):

    response = client.post(
        "/workshops",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "title": "FastAPI Workshop",
            "description": "FastAPI Basics",
            "speaker": "Speaker",
            "date": "2030-03-15",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "price": 500,
            "capacity": capacity
        }
    )

    assert response.status_code == 201

    return response.json()["id"]


def test_successful_registration(
    client,
    participant_token,
    admin_token
):

    workshop_id = create_workshop(
        client,
        admin_token
    )

    response = client.post(
        "/registrations",
        headers={
            "Authorization": f"Bearer {participant_token}"
        },
        json={
            "workshop_id": workshop_id
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["workshop_id"] == workshop_id
    assert data["status"] == "PENDING"


def test_duplicate_registration(
    client,
    participant_token,
    admin_token
):

    workshop_id = create_workshop(
        client,
        admin_token
    )

    headers = {
        "Authorization": f"Bearer {participant_token}"
    }

    first_response = client.post(
        "/registrations",
        headers=headers,
        json={
            "workshop_id": workshop_id
        }
    )

    assert first_response.status_code == 201

    response = client.post(
        "/registrations",
        headers=headers,
        json={
            "workshop_id": workshop_id
        }
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Already registered for this workshop"
    )


def test_full_workshop(
    client,
    participant_token,
    admin_token
):

    workshop_id = create_workshop(
        client,
        admin_token,
        capacity=1
    )

    first_response = client.post(
        "/registrations",
        headers={
            "Authorization": f"Bearer {participant_token}"
        },
        json={
            "workshop_id": workshop_id
        }
    )

    assert first_response.status_code == 201

    register_response = client.post(
        "/auth/register",
        json={
            "full_name": "Second Participant",
            "email": "second@test.com",
            "password": "password123",
            "role": "participant"
        }
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "second@test.com",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    second_token = login_response.json()["access_token"]

    response = client.post(
        "/registrations",
        headers={
            "Authorization": f"Bearer {second_token}"
        },
        json={
            "workshop_id": workshop_id
        }
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        == "Workshop is full"
    )


def test_unauthorized_registration_access(
    client,
    participant_token,
    admin_token
):

    workshop_id = create_workshop(
        client,
        admin_token
    )

    registration_response = client.post(
        "/registrations",
        headers={
            "Authorization": f"Bearer {participant_token}"
        },
        json={
            "workshop_id": workshop_id
        }
    )

    assert registration_response.status_code == 201

    registration_id = (
        registration_response.json()["id"]
    )

    another_user = client.post(
        "/auth/register",
        json={
            "full_name": "Another User",
            "email": "another@test.com",
            "password": "password123",
            "role": "participant"
        }
    )

    assert another_user.status_code == 201

    login_response = client.post(
        "/auth/login",
        json={
            "email": "another@test.com",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    another_token = login_response.json()["access_token"]

    response = client.get(
        f"/registrations/{registration_id}",
        headers={
            "Authorization": f"Bearer {another_token}"
        }
    )

    assert response.status_code == 403