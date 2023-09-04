def test_ping(client):
    resp = client.get("/system/ping")
    assert resp.status_code == 200
    assert resp.json == {"data": "pong"}
