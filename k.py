from fastapi import FastAPI, Depends, HTTPException
from pykerberos import client
import pyad
from pydantic import BaseModel

app = FastAPI()

# Настройка подключения к Active Directory
pyad.set_defaults(ldap_server="WindowsServer2.gazprom.ru", base_dn="DC=gazprom,DC=ru")


class User(BaseModel):
    username: str


@app.get("/login")
async def login(username: str):
    # Проверяем входные данные пользователя
    if not username:
        raise HTTPException(status_code=400, detail="Invalid credentials", headers={"WWW-Authenticate": "Negotiate"})
    try:
        # Получаем ticket от Kerberos
        ticket = client.get_ticket(
            principal=f"HTTP/{username}@YOUR.DOMAIN.COM",
            keytab_path="C:\\path\\to\\your\\keytab"
        )

        # Проверяем ticket
        client.verify_ticket(ticket)

        # Получаем информацию о пользователе из Active Directory
        ad_user = pyad.User(username=username)
        print('ad_user:', ad_user)

        # Здесь вы можете добавить дополнительную проверку или обработку
        return {"message": f"Welcome, {ad_user.full_name}!"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.get("/protected")
async def protected_route():
    # Здесь ваша защищенная логика
    return {"message": "Protected route"}
