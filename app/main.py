from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from agent_utils.agent import MedicineAsisstentAgent
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


# Response model
class AgentResponse(BaseModel):
    """Response model for agent invocation."""
    response: str
    

@app.get("/")
async def home(request: Request):
    """Serve the main HTML interface."""
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/agent", response_model=AgentResponse)
async def invoke_agent(request: AgentRequest):
    """
    Invoke the AI agent with a prompt.
    
    The agent can read and write text files based on natural language instructions.
    """
    try:
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")
        
        # Run the agent with the user's prompt
        agent = MedicineAsisstentAgent()
        return AgentResponse(response=str(agent.run_agent(request.prompt)))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error invoking agent: {str(e)}")

@app.get("/logs")
def get_logs():
    return {
        "logs": "\n".join(LOG_BUFFER)
    }

uvicorn.run(app, host="0.0.0.0", port=8888)