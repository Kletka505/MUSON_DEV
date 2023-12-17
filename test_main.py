from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_docs_main():
    response = client.get("/docs")
    assert response.status_code == 200


def test_catalog_main():
    response = client.get("/catalog")
    assert response.status_code == 200

    
def test_account_main():
    response = client.get("/account")
    assert response.status_code == 200



