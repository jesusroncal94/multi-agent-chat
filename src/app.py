from fastapi import FastAPI

from endpoints import router


def create_app():
    app = FastAPI(title="MultiAgentChatAI")
    app.include_router(router)
    return app
