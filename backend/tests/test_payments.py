from unittest.mock import Mock


def test_stripe_checkout_api(
    client,
    participant_token,
    admin_token,
    monkeypatch
):

    workshop_response = client.post(
        "/workshops",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "title": "Stripe Workshop",
            "description": "Stripe Testing",
            "speaker": "Speaker",
            "date": "2030-05-15",
            "start_time": "10:00:00",
            "end_time": "12:00:00",
            "price": 500,
            "capacity": 10
        }
    )

    assert workshop_response.status_code == 201

    workshop_id = workshop_response.json()["id"]

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

    mock_session = Mock()

    mock_session.id = "cs_test_123"
    mock_session.url = (
        "https://checkout.stripe.com/test"
    )

    def mock_create(**kwargs):
        return mock_session

    monkeypatch.setattr(
        "app.routes.payments.stripe.checkout.Session.create",
        mock_create
    )

    response = client.post(
        "/payments/create-checkout-session"
        f"?registration_id={registration_id}",
        headers={
            "Authorization": f"Bearer {participant_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "checkout_url" in data

    assert (
        data["checkout_url"]
        == "https://checkout.stripe.com/test"
    )