import uvicorn
from fastapi import FastAPI, HTTPException,Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directoty="templates")

uvicorn.run(app,host="0.0.0.0",port=8000)