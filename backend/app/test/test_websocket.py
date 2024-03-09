from fastapi.testclient import TestClient

def test_read_main():
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"msg": "Hello World"}


def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws/1/1") as websocket:
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}