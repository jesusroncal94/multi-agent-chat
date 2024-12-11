import json

import autogen
import redis
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config import settings

router = APIRouter()
redis_client = redis.Redis(
    host=settings.redis_host, port=settings.redis_port, db=settings.redis_db
)
chat_session_ttl = settings.chat_session_ttl
oai_config_list = [
    oai_config.model_dump(by_alias=True) for oai_config in settings.oai_config_list
]


@router.get("/")
def read_root():
    return {"message": "Hello from MultiAgentChatAI!"}


class ChatMessage(BaseModel):
    message: str
    session_id: str


@router.post("/chat")
async def chat_endpoint(chat_message: ChatMessage):
    try:
        # Get or create chat session
        chat_session = get_chat_session(chat_message.session_id)
        if not chat_session:
            assistant, human = create_chat_session(chat_message.session_id)
        else:
            assistant, human = chat_session

        # Get response from assistant
        chat_result = human.initiate_chat(
            assistant,
            clear_history=False,
            message=chat_message.message,
            silent=True,
        )

        # Store chat history in Redis
        redis_client.set(
            f"chat_session:{chat_message.session_id}:history",
            json.dumps(chat_result.chat_history),
            ex=int(chat_session_ttl.total_seconds()),
        )

        # Get the last assistant message
        last_message = next(
            (
                msg["content"]
                for msg in reversed(chat_result.chat_history)
                if msg["name"] == "assistant"
            ),
            "No response from assistant",
        )

        return {"session_id": chat_message.session_id, "response": last_message}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_agents():
    """Create the assistant and user agents"""
    assistant_prompt = read_file(file_path="src/prompts/assistant.prompt")
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config={"config_list": oai_config_list, "temperature": 0.7},
        system_message=assistant_prompt,
    )

    human = autogen.UserProxyAgent(
        name="customer",
        human_input_mode="NEVER",  # Disable manual interaction for API use
        max_consecutive_auto_reply=0,
        llm_config={"config_list": oai_config_list},
    )

    return assistant, human


def create_chat_session(session_id: str):
    """Create new chat session"""
    assistant, human = create_agents()

    # Initialize empty chat history
    redis_client.set(
        f"chat_session:{session_id}:history",
        json.dumps([]),
        ex=int(chat_session_ttl.total_seconds()),
    )

    return assistant, human


def get_chat_session(session_id: str):
    """Retrieve chat session"""
    chat_history = redis_client.get(f"chat_session:{session_id}:history")

    if not chat_history:
        return None

    assistant, human = create_agents()

    # Load existing chat history
    history = json.loads(chat_history)
    for msg in history:
        if msg["role"] == "assistant":
            assistant.send(msg, human, silent=True)
        else:
            human.send(msg, assistant, silent=True)

    return assistant, human


def read_file(file_path: str, as_json: bool = False) -> str:
    """Read content from a file"""
    try:
        with open(file_path, "r") as file:
            print(f"file '{file_path}' successfully loaded")
            if as_json:
                return json.load(file)
            else:
                return file.read()
    except json.JSONDecodeError:
        print(f"error decoding JSON file: {file_path}")
        return ""
    except Exception as e:
        print(f"error reading file: {e}")
        return ""
