from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent_utils.agent import MedicineAssistantAgent
from pathlib import Path
import uvicorn
from logger import LOG_BUFFER

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Request model
class AgentRequest(BaseModel):
    """Request model for agent invocation."""
    prompt: str

@app.get("/")
async def home(request: Request):
    """Serve the main HTML interface."""
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/agent")
async def invoke_agent(request: AgentRequest):
    if not request.prompt.strip():
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)