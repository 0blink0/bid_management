# Architecture

**Analysis Date:** 2026-04-20

## Pattern Overview

**Overall:** Monorepo-style split architecture (FastAPI backend + Vue SPA frontend + reserved knowledge storage), with API-first integration and Agent-oriented domain modules.

**Key Characteristics:**
- Backend entrypoint composes middleware and v1 routers centrally in `bid_tool_agents/backend/app/main.py`.
- API layer is grouped by capability modules (`agents/files/knowledge`) under `bid_tool_agents/backend/app/api/v1/`.
- Agent domain uses a shared abstract base and per-agent implementations under `bid_tool_agents/backend/app/agents/`.

## Layers

**Presentation Layer (Frontend SPA):**
- Purpose: Browser UI, route-level page composition, auth-guarded navigation.
- Location: `bid_tool_agents/frontend/src/`
- Contains: `pages`, reusable `components`, `router`, `stores`, styles.
- Depends on: Vue ecosystem, backend `/api` proxy configured in `bid_tool_agents/frontend/vite.config.ts`.
- Used by: End users via browser.

**API Layer (Backend HTTP):**
- Purpose: Expose HTTP endpoints and request/response contracts.
- Location: `bid_tool_agents/backend/app/api/v1/`
- Contains: `agents.py`, `files.py`, `knowledge.py`, `router.py`.
- Depends on: FastAPI and configuration singleton from `bid_tool_agents/backend/app/config.py`.
- Used by: Frontend and external API clients.

**Application/Orchestration Layer (Agents):**
- Purpose: Organize task orchestration and specialized processing units.
- Location: `bid_tool_agents/backend/app/agents/`
- Contains: `coordinator`, `parser`, `compliance`, `comparison`, `qualification`, `risk`, `evaluation`, `expert`, `archive`, `statistics`, plus `base`.
- Depends on: Base agent contract and tool modules such as `bid_tool_agents/backend/app/tools/llm/`.
- Used by: API layer (intended via `/agents` endpoints).

**Infrastructure/Tools Layer:**
- Purpose: Encapsulate LLM providers, document parsing, and data-store clients.
- Location: `bid_tool_agents/backend/app/tools/`
- Contains: `llm`, `document`, `database` submodules.
- Depends on: External SDKs declared in `bid_tool_agents/backend/pyproject.toml`.
- Used by: Agent implementations (for example parser agent imports LLM manager).

**Configuration Layer:**
- Purpose: Centralized runtime settings, environment selection, and storage/DB/LLM config model.
- Location: `bid_tool_agents/backend/app/config.py` and `bid_tool_agents/backend/config/*.yaml`.
- Contains: Typed `Settings` and per-domain config classes.
- Depends on: `pydantic-settings`, YAML files, and environment variables.
- Used by: Backend app bootstrap and API modules.

## Data Flow

**User Review Request Flow:**

1. Frontend route/page initiates API call through `/api` (proxied by Vite in `bid_tool_agents/frontend/vite.config.ts`).
2. FastAPI app receives request through router chain in `bid_tool_agents/backend/app/main.py` and `bid_tool_agents/backend/app/api/v1/router.py`.
3. Capability endpoint (`agents/files/knowledge`) validates payload with Pydantic models and returns typed response in `bid_tool_agents/backend/app/api/v1/*.py`.
4. Agent execution path (current design) delegates to agent classes deriving from `BaseAgent` in `bid_tool_agents/backend/app/agents/base/agent.py`.
5. Agent stores immediate + short-term context via memory package `bid_tool_agents/backend/app/agents/base/memory/` and returns result to API layer.

**State Management:**
- Frontend auth/session state uses Pinia store in `bid_tool_agents/frontend/src/stores/user.ts`.
- Backend runtime settings are cached singleton via `get_settings()` in `bid_tool_agents/backend/app/config.py`.
- Agent runtime state is encapsulated by `AgentMemory` in `bid_tool_agents/backend/app/agents/base/memory/core.py`.

## Key Abstractions

**BaseAgent Contract:**
- Purpose: Unified lifecycle (`initialize`/`invoke`), graph construction, and memory integration.
- Examples: `bid_tool_agents/backend/app/agents/base/agent.py`, `bid_tool_agents/backend/app/agents/coordinator/agent.py`, `bid_tool_agents/backend/app/agents/parser/agent.py`.
- Pattern: Template method + abstract methods for graph/process specialization.

**Agent Workflow Graph:**
- Purpose: Represent multi-step processing pipelines as explicit nodes/edges.
- Examples: `CoordinatorAgent._build_graph()` in `bid_tool_agents/backend/app/agents/coordinator/agent.py`, `ParserAgent._build_graph()` in `bid_tool_agents/backend/app/agents/parser/agent.py`.
- Pattern: LangGraph StateGraph-based orchestration.

**LLMManager:**
- Purpose: Register, select, and route among multiple LLM backends.
- Examples: `bid_tool_agents/backend/app/tools/llm/manager.py`.
- Pattern: Registry + runtime routing rules + façade methods (`chat`, `chat_stream`, `embeddings`).

## Entry Points

**Backend App Entry Point:**
- Location: `bid_tool_agents/backend/app/main.py`
- Triggers: Uvicorn/FastAPI startup.
- Responsibilities: Create app, bind CORS, include API router, expose root and health checks.

**Backend API Router Aggregation:**
- Location: `bid_tool_agents/backend/app/api/v1/router.py`
- Triggers: Included by backend app with `/api/v1` prefix from config.
- Responsibilities: Compose module routers for agents/files/knowledge.

**Frontend SPA Entry Point:**
- Location: `bid_tool_agents/frontend/src/main.ts`
- Triggers: Browser app bootstrap.
- Responsibilities: Mount Vue app, install Pinia/router/Naive UI/charts plugin.

## Error Handling

**Strategy:** Endpoint-level validation and exception signaling with explicit HTTP status codes; domain agents currently return structured success/error dictionaries.

**Patterns:**
- Raise `HTTPException` for input validation failures in file upload flow (`bid_tool_agents/backend/app/api/v1/files.py`).
- Catch broad exceptions and convert to response payload in agent invoke API (`bid_tool_agents/backend/app/api/v1/agents.py`).

## Cross-Cutting Concerns

**Logging:** Startup/shutdown currently uses simple `print` statements in `bid_tool_agents/backend/app/main.py`; logging config fields exist in `bid_tool_agents/backend/app/config.py`.
**Validation:** Request schemas are defined via Pydantic models in `bid_tool_agents/backend/app/api/v1/*.py`.
**Authentication:** Frontend route access control uses navigation guard and Pinia auth flag in `bid_tool_agents/frontend/src/router/index.ts` and `bid_tool_agents/frontend/src/stores/user.ts`; backend auth middleware is not detected in current API entry chain.

---

*Architecture analysis: 2026-04-20*
# Architecture

**Analysis Date:** 2026-04-20

## Pattern Overview

**Overall:** Layered modular monolith with agent-oriented orchestration

**Key Characteristics:**
- HTTP API composition is centralized in `bid_tool_agents/backend/app/main.py` and `bid_tool_agents/backend/app/api/v1/router.py`.
- Domain behavior is split into specialized agent modules under `bid_tool_agents/backend/app/agents/` that share a common base contract.
- Frontend routing and page composition are feature-oriented in `bid_tool_agents/frontend/src/router/index.ts` and `bid_tool_agents/frontend/src/pages/`.

## Layers

**Frontend Application Layer:**
- Purpose: Render pages, guard routes, and invoke backend endpoints.
- Location: `bid_tool_agents/frontend/src/`
- Contains: Vue app bootstrap, route table, Pinia auth state, layout/components/pages.
- Depends on: Vue, Vue Router, Pinia, Naive UI, backend `/api/v1/*` endpoints via proxy in `bid_tool_agents/frontend/vite.config.ts`.
- Used by: Browser clients.

**API Layer:**
- Purpose: Expose HTTP contracts and validate request/response models.
- Location: `bid_tool_agents/backend/app/api/v1/`
- Contains: Route aggregators and endpoint modules (`agents.py`, `files.py`, `knowledge.py`).
- Depends on: FastAPI, Pydantic models, app configuration in `bid_tool_agents/backend/app/config.py`.
- Used by: Frontend pages/components (for example upload in `bid_tool_agents/frontend/src/pages/Upload.vue`).

**Agent Orchestration Layer:**
- Purpose: Define reusable agent lifecycle and task orchestration flow.
- Location: `bid_tool_agents/backend/app/agents/`
- Contains: `BaseAgent`, coordinator agent, specialist agents (parser/compliance/risk/etc).
- Depends on: LangGraph, memory subsystem, LLM manager.
- Used by: API agent invocation flow and tests in `bid_tool_agents/backend/tests/agents/`.

**Memory & Tooling Layer:**
- Purpose: Provide cross-agent state handling and infrastructure adapters.
- Location: `bid_tool_agents/backend/app/agents/base/memory/` and `bid_tool_agents/backend/app/tools/`
- Contains: four-layer memory classes, LLM registry/manager, database and document tool modules.
- Depends on: Python stdlib threading/datetime, provider implementations, external service SDKs.
- Used by: Base and specialist agents.

**Configuration Layer:**
- Purpose: Resolve environment-specific runtime settings and service endpoints.
- Location: `bid_tool_agents/backend/app/config.py` and `bid_tool_agents/backend/config/*.yaml`
- Contains: strongly-typed settings models, YAML loader, environment switch.
- Depends on: pydantic-settings, YAML files, `ENV` environment variable.
- Used by: FastAPI app bootstrap, API endpoints, tests.

## Data Flow

**Web Request to Agent Processing:**

1. Frontend sends requests to `/api/v1/*` (example: file upload in `bid_tool_agents/frontend/src/pages/Upload.vue`) through Vite proxy in `bid_tool_agents/frontend/vite.config.ts`.
2. FastAPI app in `bid_tool_agents/backend/app/main.py` dispatches requests to versioned routers via `app.include_router(...)`.
3. Endpoint handlers in `bid_tool_agents/backend/app/api/v1/*.py` parse request models and call processing logic (currently partial stubs in multiple endpoints).
4. Agent execution uses `BaseAgent.invoke()` in `bid_tool_agents/backend/app/agents/base/agent.py`, which records immediate memory, calls `process()`, then updates short-term memory.
5. Results are returned as response models to frontend consumers.

**State Management:**
- Frontend auth state is local and token-based in `bid_tool_agents/frontend/src/stores/user.ts`.
- Backend task/agent state is in-memory by default through four-layer memory classes in `bid_tool_agents/backend/app/agents/base/memory/`.

## Key Abstractions

**BaseAgent Contract:**
- Purpose: Enforce consistent lifecycle (`initialize`, `invoke`, `process`) and graph wiring.
- Examples: `bid_tool_agents/backend/app/agents/base/agent.py`, `bid_tool_agents/backend/app/agents/parser/agent.py`, `bid_tool_agents/backend/app/agents/coordinator/agent.py`
- Pattern: Template method + subclass specialization.

**AgentMemory Aggregate:**
- Purpose: Encapsulate immediate/short-term/long-term/core memory capabilities per agent.
- Examples: `bid_tool_agents/backend/app/agents/base/memory/core.py`, `bid_tool_agents/backend/app/agents/base/memory/short_term.py`
- Pattern: Composition over inheritance.

**LLMManager Registry Facade:**
- Purpose: Manage provider registration, default selection, and optional routing.
- Examples: `bid_tool_agents/backend/app/tools/llm/manager.py`, `bid_tool_agents/backend/app/tools/llm/registry.py`
- Pattern: Registry + manager facade.

## Entry Points

**FastAPI Runtime Entry:**
- Location: `bid_tool_agents/backend/app/main.py`
- Triggers: `uvicorn app.main:app --reload` or equivalent ASGI startup.
- Responsibilities: App construction, CORS middleware, API router registration, lifecycle hooks.

**Frontend Runtime Entry:**
- Location: `bid_tool_agents/frontend/src/main.ts`
- Triggers: Vite `npm run dev` / production bundle startup.
- Responsibilities: Vue app creation, plugin registration, router mount.

**Route Composition Entry:**
- Location: `bid_tool_agents/frontend/src/router/index.ts`
- Triggers: Every navigation event.
- Responsibilities: Feature route map, auth guard redirects.

## Error Handling

**Strategy:** Endpoint-level validation and explicit HTTP errors, with fallback placeholders where implementation is pending.

**Patterns:**
- File upload rejects invalid size/type via `HTTPException` in `bid_tool_agents/backend/app/api/v1/files.py`.
- Agent invoke endpoint wraps logic in `try/except` and returns structured error fields in `bid_tool_agents/backend/app/api/v1/agents.py`.

## Cross-Cutting Concerns

**Logging:** Startup/shutdown logging via `print` in `bid_tool_agents/backend/app/main.py`; no centralized logger wiring detected in runtime path.
**Validation:** Pydantic request/response models in `bid_tool_agents/backend/app/api/v1/*.py` and typed settings in `bid_tool_agents/backend/app/config.py`.
**Authentication:** Frontend route guard uses local token state in `bid_tool_agents/frontend/src/stores/user.ts`; backend auth middleware or auth routers are not detected in current API package.

---

*Architecture analysis: 2026-04-20*
