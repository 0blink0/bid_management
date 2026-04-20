# Codebase Structure

**Analysis Date:** 2026-04-20

## Directory Layout

```
ai_bid_management/
├── bid_tool_agents/               # Main application workspace (backend + frontend + docs)
│   ├── backend/                   # FastAPI + Agent domain backend
│   ├── frontend/                  # Vue 3 SPA frontend
│   ├── knowledge_base/            # Reserved knowledge repository (currently minimal)
│   ├── docs/                      # Product/engineering docs for subproject
│   └── docker-compose.yaml        # Local multi-service orchestration
├── docs/                          # Project-level documentation
├── .planning/codebase/            # Generated architecture mapping docs
└── README.md                      # Root project summary
```

## Directory Purposes

**`bid_tool_agents/backend`:**
- Purpose: Hosts backend API server and Agent-oriented application logic.
- Contains: `app/`, `tests/`, Python packaging/config files.
- Key files: `bid_tool_agents/backend/app/main.py`, `bid_tool_agents/backend/app/config.py`, `bid_tool_agents/backend/pyproject.toml`.

**`bid_tool_agents/backend/app`:**
- Purpose: Core backend source modules.
- Contains: `api`, `agents`, `tools`, `memory`, `models`, `services`, `skills`.
- Key files: `bid_tool_agents/backend/app/api/v1/router.py`, `bid_tool_agents/backend/app/agents/base/agent.py`.

**`bid_tool_agents/frontend/src`:**
- Purpose: Frontend application source.
- Contains: `pages`, `components`, `router`, `stores`, `styles`.
- Key files: `bid_tool_agents/frontend/src/main.ts`, `bid_tool_agents/frontend/src/router/index.ts`, `bid_tool_agents/frontend/src/App.vue`.

**`bid_tool_agents/backend/tests`:**
- Purpose: Backend test suite (primarily agent behavior and memory integration).
- Contains: `agents/` tests plus shared `conftest.py`.
- Key files: `bid_tool_agents/backend/tests/agents/test_parser.py`, `bid_tool_agents/backend/tests/conftest.py`.

## Key File Locations

**Entry Points:**
- `bid_tool_agents/backend/app/main.py`: FastAPI app factory and router mounting.
- `bid_tool_agents/frontend/src/main.ts`: Vue app bootstrap.
- `bid_tool_agents/frontend/index.html`: Frontend host document for Vite build.

**Configuration:**
- `bid_tool_agents/backend/app/config.py`: Unified typed settings.
- `bid_tool_agents/backend/config/development.yaml`: Environment-specific YAML config.
- `bid_tool_agents/frontend/vite.config.ts`: Frontend aliasing and API proxy.
- `bid_tool_agents/backend/pytest.ini`: Test runtime config.

**Core Logic:**
- `bid_tool_agents/backend/app/agents/`: Agent implementations by domain.
- `bid_tool_agents/backend/app/tools/`: LLM/document/database integrations.
- `bid_tool_agents/backend/app/api/v1/`: HTTP API contracts and routes.
- `bid_tool_agents/frontend/src/pages/`: Route-level UI screens.

**Testing:**
- `bid_tool_agents/backend/tests/agents/`: Agent-focused unit/async tests.
- `bid_tool_agents/backend/tests/conftest.py`: Shared test bootstrap.

## Naming Conventions

**Files:**
- Python modules use `snake_case.py` (example: `bid_tool_agents/backend/app/api/v1/knowledge.py`).
- Vue components use `PascalCase.vue` (example: `bid_tool_agents/frontend/src/components/layout/AppLayout.vue`).
- Frontend TS utility/store/router files use lowercase names (example: `bid_tool_agents/frontend/src/stores/user.ts`).

**Directories:**
- Backend feature directories are domain-oriented lowercase (example: `bid_tool_agents/backend/app/agents/coordinator/`).
- Frontend organizes by role (`pages`, `components`, `router`, `stores`) in `bid_tool_agents/frontend/src/`.

## Where to Add New Code

**New Feature:**
- Primary backend API endpoint: `bid_tool_agents/backend/app/api/v1/` (new module + include in `router.py`).
- Primary backend domain logic: `bid_tool_agents/backend/app/agents/<feature>/`.
- Frontend route page: `bid_tool_agents/frontend/src/pages/`.
- Tests: `bid_tool_agents/backend/tests/agents/` for agent behavior and endpoint-linked logic.

**New Component/Module:**
- Shared UI component: `bid_tool_agents/frontend/src/components/<domain>/`.
- New frontend route registration: `bid_tool_agents/frontend/src/router/index.ts`.
- New backend integration wrapper: `bid_tool_agents/backend/app/tools/<provider>/`.

**Utilities:**
- Agent-shared capabilities: place in `bid_tool_agents/backend/app/tools/` (IO/integration) or `bid_tool_agents/backend/app/skills/` (domain algorithm).
- Frontend shared state: `bid_tool_agents/frontend/src/stores/`.

## Special Directories

**`.planning/codebase`:**
- Purpose: Persistent architecture/quality/stack mapping output for planning automation.
- Generated: Yes (by mapping workflows/agents).
- Committed: Yes.

**`bid_tool_agents/knowledge_base`:**
- Purpose: Dedicated location reserved for knowledge assets.
- Generated: No.
- Committed: Yes.

**`bid_tool_agents/backend/app/services`:**
- Purpose: Reserved service-layer namespace for business orchestration abstractions.
- Generated: No.
- Committed: Yes (currently placeholder-only).

---

*Structure analysis: 2026-04-20*
# Codebase Structure

**Analysis Date:** 2026-04-20

## Directory Layout

```text
ai_bid_management/
├── bid_tool_agents/               # Application code (frontend + backend + tests)
│   ├── frontend/                  # Vue3 UI application
│   │   ├── src/
│   │   │   ├── pages/             # Route-level page views
│   │   │   ├── components/        # Reusable UI pieces by domain
│   │   │   ├── router/            # Router table and guards
│   │   │   └── stores/            # Pinia state stores
│   └── backend/                   # FastAPI + agent system
│       ├── app/
│       │   ├── api/v1/            # HTTP endpoints
│       │   ├── agents/            # Agent orchestration and specializations
│       │   ├── tools/             # LLM/document/database adapters
│       │   └── main.py            # FastAPI entrypoint
│       ├── config/                # Environment YAML configs
│       └── tests/                 # Pytest suites and fixtures
├── docs/                          # Product, API, and dataset docs
└── .planning/codebase/            # Generated codebase mapping artifacts
```

## Directory Purposes

**`bid_tool_agents/frontend/src/pages`:**
- Purpose: User-facing workflows as top-level screens.
- Contains: One `.vue` per route concern (e.g., upload/reports/knowledge/admin).
- Key files: `bid_tool_agents/frontend/src/pages/Upload.vue`, `bid_tool_agents/frontend/src/pages/KnowledgeBase.vue`

**`bid_tool_agents/frontend/src/components`:**
- Purpose: Reusable UI modules grouped by domain (`layout`, `knowledge`, `report`, `common`, `task`, `file`).
- Contains: Presentational and compositional Vue components.
- Key files: `bid_tool_agents/frontend/src/components/layout/AppLayout.vue`, `bid_tool_agents/frontend/src/components/file/FileUploader.vue`

**`bid_tool_agents/backend/app/api/v1`:**
- Purpose: API contract layer.
- Contains: Router aggregation and endpoint handlers.
- Key files: `bid_tool_agents/backend/app/api/v1/router.py`, `bid_tool_agents/backend/app/api/v1/files.py`

**`bid_tool_agents/backend/app/agents`:**
- Purpose: Multi-agent domain logic with shared contract.
- Contains: `base` abstractions, coordinator, and specialist agent implementations.
- Key files: `bid_tool_agents/backend/app/agents/base/agent.py`, `bid_tool_agents/backend/app/agents/coordinator/agent.py`, `bid_tool_agents/backend/app/agents/parser/agent.py`

**`bid_tool_agents/backend/app/tools`:**
- Purpose: Integration adapters for LLM and data/document infrastructure.
- Contains: Provider manager/registry and service-specific helper modules.
- Key files: `bid_tool_agents/backend/app/tools/llm/manager.py`, `bid_tool_agents/backend/app/tools/database/postgres.py`

## Key File Locations

**Entry Points:**
- `bid_tool_agents/backend/app/main.py`: FastAPI app factory and API mount.
- `bid_tool_agents/frontend/src/main.ts`: Vue app bootstrap.
- `bid_tool_agents/frontend/src/router/index.ts`: route definitions and auth guard.

**Configuration:**
- `bid_tool_agents/backend/app/config.py`: typed settings + YAML loader.
- `bid_tool_agents/backend/config/development.yaml`: development environment values and service blocks.
- `bid_tool_agents/frontend/vite.config.ts`: dev server, alias, and API proxy.

**Core Logic:**
- `bid_tool_agents/backend/app/agents/base/agent.py`: shared invoke/process lifecycle.
- `bid_tool_agents/backend/app/agents/base/memory/core.py`: memory model aggregation.
- `bid_tool_agents/backend/app/tools/llm/manager.py`: LLM orchestration/routing.

**Testing:**
- `bid_tool_agents/backend/tests/agents/`: per-agent test suites.
- `bid_tool_agents/backend/tests/agents/conftest.py`: agent test fixtures/mocks.
- `bid_tool_agents/backend/run_agent_test.py`: command wrapper for focused test execution.

## Naming Conventions

**Files:**
- Backend Python modules use `snake_case` (`short_term.py`, `run_agent_test.py`).
- Frontend components/pages use `PascalCase.vue` (`ReportDetail.vue`, `AppSidebar.vue`).
- Route/store modules use `index.ts` or descriptive `camelCase` filenames (`user.ts`).

**Directories:**
- Domain-first grouping under both frontend and backend (`agents/parser`, `components/report`).
- Versioned API directory pattern under backend (`api/v1`).

## Where to Add New Code

**New Feature:**
- Primary backend API contract: `bid_tool_agents/backend/app/api/v1/`
- Primary backend implementation: `bid_tool_agents/backend/app/agents/` (new agent) or `bid_tool_agents/backend/app/tools/` (integration helper)
- Frontend page entry: `bid_tool_agents/frontend/src/pages/`
- Tests: `bid_tool_agents/backend/tests/agents/` for agent behavior and shared fixture adjustments in `bid_tool_agents/backend/tests/agents/conftest.py`

**New Component/Module:**
- Layout/navigation UI: `bid_tool_agents/frontend/src/components/layout/`
- Feature-scoped reusable UI: matching domain folder in `bid_tool_agents/frontend/src/components/` (for example `knowledge` or `report`)

**Utilities:**
- Backend shared infrastructure helpers: `bid_tool_agents/backend/app/tools/`
- Frontend cross-page state: `bid_tool_agents/frontend/src/stores/`

## Special Directories

**`docs/`:**
- Purpose: Product flows, API reference, and sample datasets.
- Generated: No.
- Committed: Yes.

**`bid_tool_agents/backend/config/`:**
- Purpose: Environment-specific runtime configuration files loaded by `app/config.py`.
- Generated: No.
- Committed: Yes.

**`.planning/codebase/`:**
- Purpose: Persistent architectural reference for future planning/execution commands.
- Generated: Yes.
- Committed: Yes.

---

*Structure analysis: 2026-04-20*
