from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    # basic checks
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure clean state for the test
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # 1) Signup should succeed
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200, res.text
    assert email in activities[activity]["participants"]

    # 2) Signing up again should return 400 (already signed up)
    res2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert res2.status_code == 400

    # 3) Unregister should succeed
    res3 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert res3.status_code == 200
    assert email not in activities[activity]["participants"]

    # 4) Unregistering again should return 404
    res4 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert res4.status_code == 404
