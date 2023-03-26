import pandas as pd
import os

from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import FileResponse

from typing import Annotated
from src.backend.database import engine
from src.backend.internals.users import get_password_hash
from pathlib import Path


app = APIRouter()
TRUE_PASSWORD = "$5$rounds=10000$myVerySecretSalt$R11dtiQzOx8103YIoCSjqdPVous.U6xO8noZACy3tb0"


@app.get("/users/export", status_code=200)
async def get_users_xlsx(password: Annotated[str, Form()]):

    if get_password_hash(password) == TRUE_PASSWORD:

        data_dir = Path(__file__).parent.parent.parent.parent / "users_data"
        file_path = data_dir / "users.xlsx"

        if os.path.exists(file_path):
            os.remove(file_path)
        data_dir.mkdir(exist_ok=True)

        connection = engine.raw_connection()
        df = pd.read_sql("SELECT user.id, user.nickname, user.deleted, user.user_email, usermetadata.description, " 
                         "usermetadata.photo from user, usermetadata WHERE user.id=usermetadata.user_id",
                         con=connection)
        df.to_excel(file_path, index=False)

        return FileResponse(path=file_path, filename='ActNowUsers.xlsx', media_type='multipart/form-data')
        
    else:
        
        raise HTTPException(status_code=403)

