from httpx import AsyncClient

import pytest

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "email_ID, password, time_zone, status_code",
    [
        pytest.param("", "2703mohit", "Asia/Kolkata", 422, id="missing_email"),
        pytest.param("mohited@gmail.com", "", "Asia/Kolkata", 422, id="missing_password"),
        pytest.param("mohitdg@gmail.com", "2703mohit", "", 422, id="missing_timezone"),
    ],
)
async def test_user_registration_validation(email_ID, password, time_zone, status_code):
    """Test user registration endpoint with missing fields"""
    
    async with AsyncClient(base_url="http://localhost:8000/login") as ac:
        request_data = {
            "email_ID": email_ID,
            "password": password,
            "time_zone": time_zone,
        }
        response = await ac.post(f"http://localhost:8000/login", json=request_data)
        
        # Check status code
        assert response.status_code == status_code, f"Unexpected status: {response.status_code}, body: {response.text}"

        # Optional: If your API returns error messages, assert on expected response
        if status_code == 422:
            json_response = response.json()
            assert "detail" in json_response, f"Expected validation error, got: {json_response}"
