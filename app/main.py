from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from agent_utils.agent import MedicineAssistantAgent
from logger import LOG_BUFFER
from pathlib import Path
import uvicorn

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/")
async def home(request: str):
    """Serve the main HTML interface."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/agent")
async def invoke_agent(request: str):
    if not request.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    agent = MedicineAssistantAgent()

    def stream():
        try:
            for chunk in agent.run_agent_stream(request.prompt):
                yield chunk
        except Exception as e:
            yield f"\n[ERROR] {str(e)}"

    return StreamingResponse(
        stream(),
        media_type="text/plain"
    )

@app.get("/logs")
def get_logs():
    return {
        "logs": "\n".join(LOG_BUFFER)
    }

uvicorn.run(app, host="0.0.0.0", port=8888)