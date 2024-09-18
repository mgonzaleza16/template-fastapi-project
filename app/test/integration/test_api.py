import pytest
from loguru import logger


@pytest.mark.asyncio
async def test_get_all_users(async_client):
    """
    Test to verify the endpoint for retrieving all users, sends a GET request to the /api/1.0/users/all endpoint.
    Asserts that the status code is 200.
    Verifies that the response contains a non-empty list of users.
    Logs the response details and test success.
    """
    logger.info("Starting test: test_get_all_users.")
    logger.debug("Attempting to retrieve of all users...")

    response = await async_client.get("/api/1.0/users/all")

    logger.debug(f"Response received: {response.status_code} - {response.json()}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert data is not None, "Response data should not be None"
    assert isinstance(data, list), "Response should be a list"
    assert len(data) > 0, "User list should not be empty"

    first_user = data[0]
    assert "name" in first_user, "User should have a 'name' field"
    assert "email" in first_user, "User should have a 'name' field"
    assert "uuid" in first_user, "User should have a 'name' field"

    assert isinstance(first_user["name"], str), "User 'name' should be a string"
    assert isinstance(first_user["email"], str), "User 'name' should be a string"
    assert isinstance(first_user["uuid"], str), "User 'name' should be a string"

    logger.info("Finalizing test: test_get_all_users.")


@pytest.mark.asyncio
async def test_find_by_email(async_client):
    """
    Test to verify the endpoint for retrieving a user by email, sends a GET request to the /api/1.0/users/ endpoint
    with the email as a query parameter.
    Asserts that the status code is 200.
    Verifies that the response is a dictionary containing the expected user's details.
    Ensures that the response includes the required fields: 'uuid', 'name', and 'email', and that they are of type string.
    Logs the response details and test success.
    """
    logger.info("Starting test: test_find_by_email.")
    logger.debug("Attempting to retrieve of user by email...")

    email_to_search = "ESTEBAN.LUISS7@GMAIL.COM"

    response = await async_client.get("/api/1.0/users/", params={"email": email_to_search})
    status_code = response.status_code
    response_data = response.json()

    logger.debug(f"Response received: {status_code} - {response_data}")

    assert status_code == 200, f"Expected status code 200, got {status_code}"

    assert isinstance(response_data, dict), f"Expected response data to be a dictionary, got {type(response_data)}"

    assert response_data["email"] == email_to_search, f"Expected email {email_to_search}, got {response_data['email']}"

    required_fields = ["name", "email", "uuid"]
    for field in required_fields:
        assert field in response_data, f"User should have a '{field}' field"
        assert isinstance(response_data[field], str), f"User '{field}' should be a string"

    logger.info("Finalizing test: test_find_by_email.")
