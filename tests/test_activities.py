import urllib.parse


def test_get_activities_returns_data(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success_adds_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    url = f"/activities/{urllib.parse.quote(activity)}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    participants = client.get("/activities").json()[activity]["participants"]
    assert email in participants


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # pre-existing participant
    url = f"/activities/{urllib.parse.quote(activity)}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_remove_participant_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    url = f"/activities/{urllib.parse.quote(activity)}/participants"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"
    participants = client.get("/activities").json()[activity]["participants"]
    assert email not in participants


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "doesnotexist@mergington.edu"
    url = f"/activities/{urllib.parse.quote(activity)}/participants"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
