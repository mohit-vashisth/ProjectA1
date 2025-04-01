from httpx import AsyncClient

import pytest

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_name, email_ID, password, time_zone, privacy_link, contact_number, status_code",
    [
        pytest.param("Mohit", "", "2703mohit", "Kolkata/Asia", True, "+91 8901660008", 422, id="missing_email"),
        pytest.param("Mohit", "mohit@gmail.com", "", "Kolkata/Asia", True, "+91 8901660008", 422, id="missing_password"),
        pytest.param("Mohit", "mohit@gmail.com", "2703mohit", "", True, "+91 8901660008", 422, id="missing_timezone"),
        pytest.param("Mohit", "mohit@gmail.com", "2703mohit", "Kolkata/Asia", False, "+91 8901660008", 422, id="privacy_not_accepted"),
        pytest.param("Mohit", "mohit@gmail.com", "2703mohit", "Kolkata/Asia", True, "", 422, id="missing_contact_number"),
        pytest.param("", "mohit@gmail.com", "2703mohit", "Kolkata/Asia", True, "+91 8901660008", 422, id="missing_username"),
    ],
)
async def test_user_registration_validation(user_name, email_ID, password, time_zone, privacy_link, contact_number, status_code):
    """Test user registration endpoint with missing fields"""
    
    async with AsyncClient(base_url="http://localhost:8000/signup") as ac:
        request_data = {
            "user_name": user_name,
            "email_ID": email_ID,
            "password": password,
            "time_zone": time_zone,
            "privacy_link": privacy_link,
            "contact_number": contact_number,
        }
        response = await ac.post(f"http://localhost:8000/signup", json=request_data)
        
        # Check status code
        assert response.status_code == status_code, f"Unexpected status: {response.status_code}, body: {response.text}"

        # Optional: If your API returns error messages, assert on expected response
        if status_code == 422:
            json_response = response.json()
            assert "detail" in json_response, f"Expected validation error, got: {json_response}"
