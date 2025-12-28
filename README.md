# Wonderful-Assignment

A small Pharmacy Assistant web app that demonstrates an LLM-driven agent integrated
with a MongoDB backend and a FastAPI front-end. The agent can query inventory,
query users information, and perform purchases via callable Python tools exposed to the model.

the agent does not preform any verification

**Project layout**
- `app/` — FastAPI application, templates, and agent code
	- `agent_utils/` — agent framework, tools, and database helpers
	- `templates/` — frontend HTML (`index.html`)
	- `main.py` — FastAPI app entrypoint
	- `logger.py` — in-memory log buffer used by the UI
- `mongo/` — Dockerized MongoDB init script (`init-mongo.js`) and Dockerfile
- `docker-compose.yml` — local dev environment (app + mongo)

**Architecture overview**
- The frontend (`index.html`) provides a minimal UI to send prompts and display
	streaming output from the agent, plus a small live log pane.
- The FastAPI backend (`app/main.py`) exposes endpoints:
	- `POST /agent` — sends a user's prompt to the LLM-driven agent and streams
		the model output to the client.
	- `GET /logs` — returns log buffer that used by UI.
- The agent lives in `app/agent_utils/` and provides:
	- `BaseAgent` — wrapper around the OpenAI Responses client that manages
		conversation state and function/tool registration.
        agent side orchestraion loop is not implemented only model -> tools -> model calls.
	- `tools.py` — Python functions registered as tools the model may call (DB
		lookups, purchase operations).

- MongoDB runs in a separate container initialized from `mongo/init-mongo.js`.

**How to run**
1. Install Docker & Docker Compose.
2. From the project root run:

    docker-compose up --build

    This builds the app image and starts two containers:

    - `app`: the FastAPI server (default port 8888)
    - `mongo`: MongoDB with initial data imported from `mongo/init-mongo.js`

3. Open your browser to http://localhost:8888 to use the UI.

**Development tips**
- If you change `mongo/init-mongo.js` you must recreate the Mongo container
	(the init script runs only when the DB is created). Example to force a rebuild:

    docker-compose down -v
    docker-compose up --build
