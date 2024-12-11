# MultiAgentChatAI
Conversational AI project based on multi-agent architecture.

## Prerequisites

Make sure you have the following tools installed before starting:

- [Python 3.11+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/install/)

## Installation

### 1. Clone the repository
```bash
git clone git@github.com:jesusroncal94/MultiAgentChatAI.git
cd MultiAgentChatAI
```

### 2. Set up dependencies

#### Using `requirements.txt`

Install dependencies with `pip`:
```bash
pip install -r requirements.txt
```

#### Using Astral's `uv` (optional)

If you prefer managing dependencies with `uv`, install Astral and then synchronize:
```bash
pip install astral-py
uv sync
```

### 3. Configure the environment file

Create a `.env` file based on the provided `.env.example` file:
```bash
cp .env.example .env
```
Modify the `.env` file to include your specific configuration details.

### 4. Configure Redis

The project uses Redis for caching and internal communication. Make sure Docker and Docker Compose are installed.

#### Start Redis with `docker-compose` (recommended)

Run the following command to start Redis as defined in the `compose.yaml` file:
```bash
docker-compose up redis -d
```

#### Use an external Redis instance (optional)

If you have an external Redis instance configured, update the `.env` file:
```
REDIS_HOST=<your_redis_host>
REDIS_PORT=<your_redis_port>
```

## Running the application

1. Start the FastAPI server with virtual environment enabled:
```bash
python src/main.py
```

2. Start the FastAPI server using Astral's `uv`:
```bash
uv run src/main.py
```

2. Access the API in your browser:
   - Interactive documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc interface: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Contributions

Contributions are welcome. Please open an *issue* or submit a *pull request* if you want to improve the project.

## License

This project is licensed under the terms of the MIT license. See the `LICENSE` file for more details.
