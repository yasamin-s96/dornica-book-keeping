import uvicorn
import os
from dotenv import load_dotenv
from core.server import app

load_dotenv()

if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("APP_HOST"), port=int(os.getenv("APP_PORT")))
