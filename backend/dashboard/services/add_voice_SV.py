import os
from fastapi import APIRouter, File, HTTPException, Request, UploadFile, status
from fastapi.responses import JSONResponse
from backend.core import config
from backend.security.jwt_data_extract import get_jwt_email
from backend.security.token_verification import verify_and_refresh_token
from backend.utils.logger import init_logger

user_voice_route = APIRouter()
@user_voice_route.post(path=config.VITE_USER_VOICE_ADD_EP, status_code=status.HTTP_200_OK)
async def user_voice(request: Request, file: UploadFile = File()):
    try:
        if not file or not file.filename or not file.filename.endswith(".wav"):
            init_logger(message="No file uploaded or file with incorrect format recieved.", level="warning")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file uploaded or file with incorrect format recieved.")
        
        payload = await verify_and_refresh_token(request=request)
        email_id = get_jwt_email(decoded_token=payload)

        data = await file.read()
        
        init_logger(message="file read", level="critical")
        audio_files_dir = "backend/dashboard/services/audio_files"

        files = os.listdir(path=audio_files_dir)
        init_logger(message="file read", level="critical")
        file_count = len([f for f in files if os.path.isfile(path=os.path.join(audio_files_dir, f))])

        filename = f"3Rminds_user_audio_file_{file_count}.wav"

        with open(file=f"{audio_files_dir}/{filename}", mode="wb") as f:
            f.write(data)
        
        init_logger(message="file saved", level="critical")
        return JSONResponse(
            content={"message": "File uploaded successfully", "filename": file.filename}
        )
    
    except Exception as e:
         init_logger(message=f"Unexpected error while recieving audio file: {str(e)}", level="critical")
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error while recieving audio file.")