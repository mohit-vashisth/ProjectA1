from fastapi import HTTPException, status
from typing import Dict, Any

class DatabaseError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {detail}"
        )

class DocumentNotFoundError(HTTPException):
    def __init__(self, document_type: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{document_type} not found"
        ) 