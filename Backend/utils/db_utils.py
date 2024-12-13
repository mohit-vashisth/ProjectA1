from typing import Type, TypeVar
from beanie import Document
from fastapi import HTTPException

T = TypeVar('T', bound=Document)

async def get_document_or_404(model: Type[T], query: dict) -> T:
    """Utility function to get a document or raise 404"""
    doc = await model.find_one(query)
    if not doc:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return doc

async def safe_delete_document(model: Type[T], query: dict) -> bool:
    """Safely delete a document"""
    doc = await model.find_one(query)
    if doc:
        await doc.delete()
        return True
    return False 