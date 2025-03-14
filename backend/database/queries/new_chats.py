import uuid
from fastapi import HTTPException, status, Request, Response
from backend.database.queries.user_queries import get_user
from backend.schemas.chat_schema import Chat, Chats
from backend.security.create_n_verify_chat_id import generate_chat_id, new_chat_name
from backend.security.jwt_data_extract import get_jwt_email
from backend.utils.logger import init_logger
from backend.utils.current_time import current_time
from beanie.exceptions import CollectionWasNotInitialized


async def create_new_chat(payload, request:Request):
    email_id = get_jwt_email(decoded_token=payload)
    
    try:
        chat_id = await generate_chat_id(email_id=email_id)
        
        chat_name = await new_chat_name(email_id=email_id)
        chat =[Chat(
                chat_id= chat_id,
                chat_name=chat_name
            )]
        if chat_name == "Voice_chat_1":
            init_logger(message="User First chat detected.")
            chats = Chats(
                email_ID= email_id,
                chat= chat
            )

            await chats.insert()
            init_logger(message=f"New chat {chat_name} created succesfully.")
            return chat_id
        doc = await Chats.find_one({"email_id": email_id})
        if doc is None:
            init_logger(message="Document not found!",level="error")
        else:
            doc = dict(doc)  # Convert ODM object to dictionary
            if "chat" not in doc:
                init_logger(message="Field 'chat' does not exist!",level="error")
            elif not isinstance(doc["chat"], list):
                init_logger(message="'chat' is not a list!",level="error")
            else:
                init_logger(message="Document structure is correct.",level="error")
        Chats.find_one({"email_id": email_id}).update({"$push":{"chat":chat}})
        
            
        init_logger(message=f"New chat {chat_name} created succesfully.")
    except HTTPException as http_exc:
        init_logger(message="Error while creating New chat.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while creating new chat"
        )
    return chat_id
