# client.py
import httpx
from typing import Any, Dict, Optional

# -----------------------------
# CONFIG
# -----------------------------
BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 30.0


# -----------------------------
# CUSTOM EXCEPTION
# -----------------------------
class APIClientError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


# -----------------------------
# CLIENT CLASS
# -----------------------------
class APIClient:
    def __init__(self):
        self.client = httpx.Client(
            base_url=BASE_URL,
            timeout=TIMEOUT,
            headers={
                "Content-Type": "application/json"
            }
        )

    # -------------------------
    # INTERNAL RESPONSE HANDLER
    # -------------------------
    def _handle_response(self, response: httpx.Response) -> Any:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise APIClientError(
                message=f"API Error: {response.text}",
                status_code=response.status_code
            ) from e

        # Safe JSON parse
        try:
            return response.json()
        except Exception:
            return response.text

    # -------------------------
    # GET
    # -------------------------
    def get(self, url: str, params: Optional[Dict] = None) -> Any:
        try:
            response = self.client.get(url, params=params)
            return self._handle_response(response)
        except httpx.RequestError as e:
            raise APIClientError(f"Request failed: {str(e)}")

    # -------------------------
    # POST
    # -------------------------
    def post(self, url: str, json: Optional[Dict] = None, data: Optional[Dict] = None, files=None) -> Any:
        try:
            response = self.client.post(
                url,
                json=json,
                data=data,
                files=files
            )
            return self._handle_response(response)
        except httpx.RequestError as e:
            raise APIClientError(f"Request failed: {str(e)}")

    # -------------------------
    # PUT
    # -------------------------
    def put(self, url: str, json: Optional[Dict] = None) -> Any:
        try:
            response = self.client.put(url, json=json)
            return self._handle_response(response)
        except httpx.RequestError as e:
            raise APIClientError(f"Request failed: {str(e)}")

    # -------------------------
    # DELETE
    # -------------------------
    def delete(self, url: str) -> Any:
        try:
            response = self.client.delete(url)
            return self._handle_response(response)
        except httpx.RequestError as e:
            raise APIClientError(f"Request failed: {str(e)}")

    # -------------------------
    # CLOSE CLIENT
    # -------------------------
    def close(self):
        self.client.close()


# -----------------------------
# SINGLETON INSTANCE
# -----------------------------
client = APIClient()