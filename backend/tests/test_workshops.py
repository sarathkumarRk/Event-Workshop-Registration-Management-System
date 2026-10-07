def test_workshop_creation(
    client,
    admin_token
):

    response = client.post(
        "/workshops",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "title": "Python Workshop",
            "description": "Python Basics",
            "speaker": "John",
            "date": "2030-01-15",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "price": 500,
            "capacity": 20
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Python Workshop"
    assert data["capacity"] == 20
    assert data["available_seats"] == 20
    assert data["status"] == "UPCOMING"


def test_workshop_pagination(
    client,
    admin_token
):

    for i in range(3):

        response = client.post(
            "/workshops",
            headers={
                "Authorization": f"Bearer {admin_token}"
            },
            json={
                "title": f"Workshop {i}",
                "description": "Test Workshop",
                "speaker": "Speaker",
                "date": "2030-02-15",
                "start_time": "10:00:00",
                "end_time": "12:00:00",
                "price": 500,
                "capacity": 10
            }
        )

        assert response.status_code == 201

    response = client.get(
        "/workshops?page=1&limit=2",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["limit"] == 2
    assert data["total"] == 3
    assert data["total_pages"] == 2