from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
import requests

app = FastAPI()


@app.post("/login")
async def login(request: Request):
    auth_url = "http://localhost:8000/login"
    data = await request.json()
    response = requests.post(auth_url, json=data)
    return response.json()


@app.get("/protected")
async def protected_route(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

        # Проверяем токен с основным приложением
        response = requests.post(
            "http://localhost:8000/validate_token", json={"token": token})
        if response.status_code == 200:
            return {"message": "Access granted"}
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized", headers={"WWW-Authenticate": "Negotiate"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
