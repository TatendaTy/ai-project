# AI Portfolio Project: Agent-Driven Fantasy Football Platform

A comprehensive AI portfolio demonstrating end-to-end development of agentic applications, from data engineering and machine learning to API design and AI agent orchestration on Microsoft Foundry.

## Overview

This project showcases a complete AI/ML development lifecycle for a **Sports World Central (SWC) Fantasy Football platform**. It integrates multiple technologies:

- **Machine Learning Models** (ONNX) for player performance prediction and acquisition strategy
- **RESTful API** built with FastAPI for fantasy football analytics
- **LangGraph Workflows** for multi-step agent reasoning
- **Microsoft Foundry Agent** with custom OpenAPI-based actions for autonomous API interaction
- **Agentic AI Design Patterns** demonstrating practical applications of modern AI frameworks

The project progresses from foundational ML model development through to production-ready agentic applications deployed on Azure's Microsoft Foundry platform.

## Highlights

- 🤖 **End-to-End Agentic Architecture** — Multi-turn agent reasoning with tool orchestration
- 📊 **Machine Learning Models** — ONNX-based player acquisition and training data analysis
- 🔌 **RESTful API Layer** — Production-ready FastAPI with SQLite backend, deployed in GitHub Codespaces
- 🧠 **LangGraph Workflows** — Sequential and parallel agent steps with state management
- 🛠️ **Custom Action Integration** — OpenAPI spec-to-Foundry agent action mapping with tooling strategies
- 📈 **Portfolio-Grade Code** — Well-documented, tested, and deployable

## Tech Stack

| Category | Technologies |
|----------|---------------|
| **Backend** | Python, FastAPI, SQLAlchemy, SQLite |
| **ML/AI** | ONNX, scikit-learn, pandas, LangGraph |
| **API & Tools** | OpenAPI 3.0, JSON Schema, REST |
| **Cloud/Deployment** | Microsoft Foundry, Azure, GitHub Codespaces |
| **DevOps** | GitHub Actions, Docker (optional) |

## Project Structure

```
ai-project/
├── api/                           # Core FastAPI application
│   ├── main.py                   # FastAPI app with SWC endpoints
│   ├── database.py               # SQLAlchemy DB setup
│   ├── models.py                 # ORM models (Player, Team, League, etc.)
│   ├── schemas.py                # Pydantic request/response schemas
│   ├── crud.py                   # CRUD operations
│   ├── requirements.txt           # API dependencies
│   ├── test_main.py              # Integration tests
│   └── test_crud.py              # CRUD unit tests
│
├── model-training/                      # ML: Player Acquisition Model
│   ├── main.py                   # ONNX model inference & training
│   ├── player_acquisition_model.ipynb
│   ├── player_training_data_full.csv
│   ├── *.onnx                    # Pre-trained models
│   └── complete/                 # Reference solutions
│
├── langchain/                      # LangGraph: Multi-Step Agent Workflows
│   ├── langgraph_notebook.ipynb
│   ├── swc_toolkit.py            # Toolkit for agent tools
│   └── complete/                 # Reference implementations
│
├── requirements.txt               # Consolidated dependencies for the full project
├── openapi.json                   # OpenAPI spec used by Foundry and agent tooling
├── openapi-simple.json            # Flattened OpenAPI spec for Foundry import
└── README.md
```

## Key Components

### 1. Sports World Central (SWC) API

A production-ready REST API for fantasy football analytics:

**Endpoints:**
- `GET /` — Health check
- `GET /v0/players/` — List all players
- `GET /v0/players/{player_id}` — Player details
- `GET /v0/performances/` — Performance statistics
- `GET /v0/teams/` — Team roster
- `GET /v0/leagues/` — League information
- `GET /v0/counts/` — Record counts
- `GET /v0/weeks/` — Game weeks

**Key Features:**
- Automatic OpenAPI/Swagger documentation
- SQLite database with SQLAlchemy ORM
- Pydantic validation for request/response schemas
- Comprehensive test coverage

### 2. Machine Learning Models

ONNX-based player acquisition prediction using scikit-learn (in `model-training/`):

**Models:**
- `acquisition_model_10.onnx` — 10th percentile acquisition cost prediction
- `acquisition_model_50.onnx` — Median acquisition cost prediction  
- `acquisition_model_90.onnx` — 90th percentile acquisition cost prediction

**Workflow:**
- Training on historical player data (`player_training_data_full.csv`)
- Inference for player acquisition strategy
- Multi-level percentile predictions for risk assessment

### 3. LangGraph Agent Workflows

Multi-step reasoning and tool orchestration (in `langchain/`):

**Implementation:**
- Sequential and parallel node execution
- State management across agent steps
- Integration with custom toolkits
- Support for complex agent loops

### 4. Microsoft Foundry Agent Integration

Agentic application deployed on Azure with OpenAPI-based tool integration:

**Architecture:**
- FastAPI application hosted in GitHub Codespaces (public URL)
- OpenAPI spec auto-generated by FastAPI
- Foundry agent with `gpt-4o` model
- Custom actions mapped from OpenAPI endpoints
- Multi-turn conversational reasoning

**Custom Tool Integration Strategy:**
- Simplified OpenAPI spec (`openapi-simple.json`) for Foundry compatibility
- Individual tool definitions for granular action mapping
- Fallback mechanisms for complex schema handling

## Architecture Diagram

```
┌─────────────────┐
│  User Chat      │
│  Interface      │
└────────┬────────┘
         │
┌────────▼────────────────────────┐
│  Microsoft Foundry Agent (gpt-4o)│
│  - Multi-turn reasoning         │
│  - Tool orchestration           │
└────────┬──────────────────────┬─┘
         │                      │
    ┌────▼──────────┐    ┌─────▼────────────┐
    │ SWC API       │    │ Internal Tools   │
    │ (OpenAPI)     │    │ (LangGraph, etc) │
    └────┬──────────┘    └──────────────────┘
         │
    ┌────▼──────────────┐
    │ FastAPI App       │
    │ - 8 endpoints     │
    │ - SQLAlchemy ORM  │
    └────┬──────────────┘
         │
    ┌────▼──────────────┐
    │ SQLite Database   │
    │ (Players, Teams,  │
    │  Leagues, Perf.)  │
    └───────────────────┘
```

## Custom Tool Creation: From OpenAPI to Foundry Actions

One key challenge was mapping a detailed OpenAPI specification into Foundry-compatible action definitions. Here's the workflow we implemented:

### Step 1: API Specification

Start with a FastAPI application that auto-generates OpenAPI documentation:

```python
app = FastAPI(
    title="Sports World Central (SWC) Fantasy Football API",
    version="0.2",
    servers=[
        {
            "url": "https://azure-api-container-hfa4e5dbfehtaad5.eastus-01.azurewebsites.net/openapi.json",
            "description": "Main server for SWC in Codespaces",
        }
    ],
)
```

### Step 2: Specification Simplification

Complex OpenAPI specs with deep nested schemas can cause Foundry import failures (HTTP 400). Solution:

- Convert OpenAPI 3.1.0 → 3.0.3 for compatibility
- Flatten nested component references
- Create `openapi.json` for reliable Foundry import

**After (conversion):**
- Inline schema definitions
- All parameters self-contained
- OpenAPI 3.0.3 compliance

### Step 3: Foundry Action Integration

Create individual tool JSONs for fallback scenarios:

```json
{
  "name": "list_players",
  "description": "Retrieve a list of all players in the SWC database",
  "parameters": {
    "type": "object",
    "properties": {
      "skip": { "type": "integer", "default": 0 },
      "limit": { "type": "integer", "default": 10 }
    }
  }
}
```

### Step 4: Validation & Testing

Verify agent can:
1. Call API endpoints via Foundry actions
2. Parse responses correctly
3. Reason about multi-step queries
4. Return results to user

## Screenshots & Validation

### Custom Tool Creation

The first step was creating a custom tool in Foundry to expose the SWC API endpoints:

![Creating agent tool](creating%20agent%20tool-1.jpg)

### Agent Setup in Foundry

Once the tool was configured, we created the SWC Fantasy Football Agent with the `gpt-4o` model and bound the custom SportsWorldCentralAPI action:

![Custom Agent successful tool creation](Custom%20Agent%20successful%20tool%20creation-2.png)

### Agent in Action

The agent successfully calls the API endpoints and returns structured data. Here the agent answers a query about teams in a fantasy league:

![Testing the custom agent](Testing%20the%20custom%20agent-3.jpg)

Example successful agent interaction:
```
User: "What teams are in Pigskin Prodigal Fantasy League?"
Agent: Calls GET /v0/teams/ via the SportsWorldCentralAPI action
Result: Returns list of 12 teams with details
```

## Skills Demonstrated

| Skill | Evidence |
|-------|----------|
| **API Design & Development** | FastAPI, OpenAPI spec, RESTful endpoints, SQLAlchemy |
| **Machine Learning** | ONNX models, scikit-learn, model inference |
| **Agentic AI** | Multi-turn reasoning, tool integration, state management |
| **Cloud Deployment** | Azure Foundry, GitHub Codespaces, public API hosting |
| **Data Management** | SQLite/SQLAlchemy, Pydantic validation, schema design |
| **Software Engineering** | Testing, documentation, error handling, versioning |
| **LangGraph Workflows** | Sequential/parallel execution, conditional logic |

## Local Setup

### Prerequisites
- Python 3.10+
- pip or poetry
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TatendaTy/ai-project.git
   cd ai-project
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install all project dependencies from the root requirements file:**
   ```bash
   pip install -r requirements.txt
   ```

The root `requirements.txt` includes the dependencies for the API, model training, and LangChain/LangGraph workflow notebooks, along with the shared SDK package used across the project.

## Running the Application

### Start the SWC API

```bash
cd api
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access the API:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health check:** http://localhost:8000/

### Run Tests

```bash
cd api
pytest test_main.py test_crud.py -v
```

### Explore ML Models

```bash
cd model-training
python main.py
```

Or open `player_acquisition_model.ipynb` in Jupyter.

### Test Agent Workflows

```bash
cd langchain
jupyter notebook langgraph_notebook_with_toolkit.ipynb
```

### Deploy to Foundry

1. Ensure API is publicly accessible (GitHub Codespaces or Azure App Service)
2. Export OpenAPI spec: `openapi.json`
3. Create Foundry agent with `gpt-4o` model
4. Import OpenAPI spec as custom action
5. Test in Foundry playground

### Working with notebooks

If you want to run the model-training or LangChain notebooks, the same root environment is sufficient because the notebook dependencies are included in `requirements.txt`.

## Deployment

### Microsoft Azure (Development/Production) - API

API is automatically available at:
```
https://azure-api-container-hfa4e5dbfehtaad5.eastus-01.azurewebsites.net/openapi.json
```

Update `openapi.json` and `api/main.py` with actual server URL.

### Azure Microsoft Foundry (Production)

1. Create Foundry resource in Azure Portal
2. Deploy agent with custom actions
3. Configure authentication and RBAC
4. Monitor agent performance in Foundry dashboards

## Key Lessons Learned

- **OpenAPI Compatibility:** Foundry prefers OpenAPI 3.0.3 with flattened schemas
- **Tool Integration:** Simplified specs often outperform detailed ones for AI import
- **Agentic Design:** Multi-step reasoning requires careful state management
- **Deployment:** Public URLs must be stable for agent tool integration
- **Testing:** Validate agent behavior in playground before production

## Notes

- Do not commit sensitive data (API keys, connection strings) to source control
- For production, use Azure Key Vault or GitHub Secrets
- The OpenAPI spec is automatically generated by FastAPI; manual edits should be reflected in code
- Foundry agents benefit from clear, single-purpose tool definitions

## Future Enhancements

- [ ] Add authentication (JWT, OAuth2)
- [ ] Implement caching with Redis
- [ ] Add telemetry and monitoring
- [ ] Scale to PostgreSQL for production
- [ ] Create Foundry-native plugins for advanced reasoning
- [ ] Add multi-language support for agent prompts

## Additional Links

- **[Repository](https://github.com/TatendaTy/ai-project)** — Full source code
- **[Issues](https://github.com/TatendaTy/ai-project/issues)** — Bug reports and feature requests
- **[FastAPI Docs](https://fastapi.tiangolo.com/)** — Framework documentation
- **[LangGraph Docs](https://langchain-ai.github.io/langgraph/)** — Workflow framework
- **[Microsoft Foundry Docs](https://learn.microsoft.com/)** — Cloud deployment platform

---

**Created by:** [TatendaTy](https://github.com/TatendaTy)  
**Last Updated:** May 2026  
**License:** See [LICENSE](LICENSE) 
