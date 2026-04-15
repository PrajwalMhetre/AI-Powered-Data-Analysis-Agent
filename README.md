# AI-Powered Data Analysis Agent

A professional B2B AI-Powered Data Analysis application. Allows users to upload CSV/Excel files or connect to SQL databases to get automated insights, visualizations, and an Executive Summary via an intelligent Agent framework.

## Key Features
- **Data Sanitization**: Automatic file cleaning and structuring.
- **Dynamic Querying**: Interact with your data using Natural Language.
- **Autonomous Insights**: Auto-generates an executive summary based on data trends.
- **Database Connectors**: Extensible architecture designed for Postgres, MongoDB, Snowflake integrations.
- **Secure Sandboxing**: Isolated Docker environment for Python code execution, robust endpoints.
- **Export Ready**: Exports data summaries to a shareable PDF.
- **Local LLM Support (Ollama)**: Optionally use zero-leak local LLMs (e.g., Llama 3) for stringent data privacy.

## Tech Stack
- Frontend: Streamlit
- Backend: FastAPI
- Agent Engine: LangChain / pandas / sqlalchemy
- Data Analysis: Pandas, Numpy

## Setup & Deployment

### Prerequisites
- Docker & Docker Compose
- API Keys (OpenAI / Anthropic) OR a locally running Ollama instance if using local models.

### Quick Start
1. Copy the example environments.
```bash
cp .env.example .env
```
2. Configure `.env` with your API keys or Ollama host settings.
3. Start the application stack with Docker Compose:
```bash
docker-compose up --build
```
4. Access the App:
- Frontend: `http://localhost:8501`
- Backend API Docs: `http://localhost:8000/docs`

## Usage Limits & Security
This application dynamically generates python code to assess data tables. Although executed in an isolated container instance, **do not map sensitive local volumes** besides the designated `data/` volume. Read-only DB users are heavily stressed for databases.
