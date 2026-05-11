from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from agent import FlowHunterAgent
import uvicorn

app = FastAPI(title="FlowHunter Agent", version="1.0.0")
agent = FlowHunterAgent()


@app.get("/")
def root():
    return {"agent": "FlowHunter", "status": "online"}


@app.get("/health")
def health():
    return {"status": "ok"}


# Virtuals Protocol вызывает этот endpoint когда агенту пишут
@app.post("/inference")
async def inference(request: Request):
    body = await request.json()

    # Virtuals передаёт сообщение в разных форматах — обрабатываем оба
    user_message = (
        body.get("message")
        or body.get("text")
        or body.get("input")
        or str(body)
    )

    response_text = agent.think(user_message)

    # Формат ответа который ожидает Virtuals
    return JSONResponse({
        "message": response_text,
        "status": "success"
    })


# Virtuals может спрашивать о возможностях агента
@app.get("/capabilities")
def capabilities():
    return {
        "name": "FlowHunter",
        "description": "Detects early capital movements across Base ecosystem in real-time",
        "capabilities": [
            "on-chain flow analysis",
            "trending token detection",
            "wallet activity monitoring",
            "market signal generation"
        ]
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
