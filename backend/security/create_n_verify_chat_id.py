
import uuid
from pydantic import EmailStr
from backend.schemas.chat_schema import Chats
from backend.utils.current_time import current_time
from backend.utils.logger import init_logger

async def generate_chat_id(email_id: EmailStr) -> str:
    date = current_time().date()
    year = f"{date.year}"
    month = f"{date.month:02}"
    day = f"{date.day:02}"
    
    while True:
        init_logger(message="generating chat_id")
        random_str = uuid.uuid4().hex[:16]
        chat_id=f"{random_str[0]}{year[0]}{random_str[1]}{year[1]}-"\
            f"{random_str[2]}{year[2]}{random_str[3]}{year[3]}-"\
            f"{random_str[4]}{month[0]}{random_str[5]}{month[1]}-"\
            f"{random_str[6]}{day[0]}{random_str[7]}{day[1]}-"\
            f"{random_str[8:]}"
        
        init_logger(message=f"chat_id generated: {chat_id}")

        chat = await verify_chat_id(chat_id=chat_id, email_id=email_id)
        if not chat:
            return chat_id
        
        init_logger(message=f"Regenerating chat_id.")
        

async def default_chat_name(email_id: str) -> str:
    chats_count = await Chats.find({"email_ID":email_id}).count()
    chat_name = f"Voice_chat_{chats_count + 1}"
    init_logger(message=f"number of user previous chats: {chats_count}, chat_name for new_chat: {chat_name}")
    return chat_name


async def verify_chat_id(chat_id: str, email_id: str) -> Chats | None:
    chat = await Chats.find_one({"email_ID": email_id, "chat_id": chat_id})
    if chat:
        init_logger(message=f"Chat found for chat id: {chat_id}")
        return chat
    return None