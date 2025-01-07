import pytest
from fastapi.testclient import TestClient 
import random, string
from src.main import app

client = TestClient(app)
chars = string.ascii_lowercase
test_mail = f"{''.join(random.choice(chars) for _ in range(12))}@test.com"

def test_create_user():
    response = client.post(
        "/register",
        json={
            "email": test_mail, 
            "password": "testpassword"
            }
    )

    assert response.status_code == 200 
    assert response.json()["email"] == test_mail

    response = client.post(
        "/register",
        json={
            "email": test_mail, 
            "password": "testpassword"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

    response = client.post(
        "/register",
        json={
            "email": f"{''.join(random.choice(chars) for _ in range(12))}@test.com", 
        }
    )

    assert response.status_code == 422


@pytest.fixture
def auth_token():
    response = client.post(
        "/token",
        data={
            "username": test_mail,
            "password": "testpassword",
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    return response.json()['access_token']


def test_post_qrcode(auth_token):
    response = client.post(
        "/qrcode",
        headers={
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "url": "https://google.com",
            "color": "green",
            "size": "10",
        }
    )

    assert response.status_code == 200


def test_qrcodes(auth_token):
    # List QrCodes
    response = client.get(
        "/qrcodes",
        headers={
            "Authorization": f"Bearer {auth_token}",
        }
    )

    assert response.status_code == 200

    # Test Update QR Metadata
    for qr in response.json():
        assert qr["url"] == "https://google.com"
        assert qr["color"] == "green"
        assert qr["size"] == "10"

        update = client.put(
            "/qrcode",
            headers={
                "Authorization": f"Bearer {auth_token}",
            },
            json={
                "url": "https://github.com",
                "color": "blue",
                "size": "15",
                "uuid": qr["uuid"]
            }
        )

        assert update.status_code == 200

    # Test Update QR Metadata with invalid uuid
    invalid_update = client.put(
        "/qrcode",
        headers={
            "Authorization": f"Bearer {auth_token}",
        },
        json={
            "url": "https://yahoo.com",
            "color": "blue",
            "size": "15",
            "uuid": "87545bbd-5ef9-478e-92b3-4a996f4a3055"
        }
    )

    assert invalid_update.status_code == 404
    assert "uuid not found for logged user" in invalid_update.json()["detail"]
    
    # Get Updated QrCodes
    response = client.get(
        "/qrcodes",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 200

    # Test if changed
    for qr in response.json():
        assert qr["url"] == "https://github.com"
        assert qr["color"] == "blue"
        assert qr["size"] == "15"

        # Test Get QR
        qr_response = client.get(
            f"/qrcode?qr_uuid={qr['uuid']}",
            headers={
                "Authorization": f"Bearer {auth_token}"
            }
        )

        assert qr_response.status_code == 200
        assert qr_response.headers["content-type"] == "image/png"

        not_authorized_response = client.get(
            f"/qrcode?qr_uuid={qr['uuid']}"
        )

        assert not_authorized_response.status_code == 401
        assert "Not authenticated" in not_authorized_response.json()["detail"]


def test_analytics(auth_token):
    response = client.get(
        "/analytics",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )

    assert response.status_code == 200
    
    for qr in response.json():
        assert qr["scans_count"] == len(qr["scans"])





