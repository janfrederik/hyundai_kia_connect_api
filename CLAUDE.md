# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

This project uses uv for package management (see `uv.lock`). Key commands:

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Linting and formatting
uv run ruff check .
uv run ruff format .

# Type checking (configured permissively)
uv run basedpyright

# Spell checking
uv run codespell

# Run a single test file
uv run pytest tests/eu_login_test.py

# Run the CLI tool
uv run bluelink --help
```

Alternative commands via Makefile (uses system pytest/flake8):
```bash
make test          # Run pytest
make lint          # Run flake8 and black checks
make coverage      # Run tests with coverage
make dist          # Build distributions
```

## Architecture Overview

### Core Design Pattern: Regional API Strategy

The codebase implements a **Strategy Pattern** where each region/brand combination has its own API implementation:

```
VehicleManager (Facade)
      │
      ▼
ApiImpl (Abstract Base)
      │
      ├─ ApiImplType1 ──────┬─ KiaUvoApiEU (Europe)
      │   (shared protocol)  ├─ KiaUvoApiCN (China)
      │                      ├─ KiaUvoApiAU (Australia)
      │                      └─ KiaUvoApiIN (India)
      │
      ├─ KiaUvoApiCA (Canada)
      ├─ KiaUvoApiUSA (USA Kia)
      ├─ HyundaiBlueLinkApiUSA (USA Hyundai/Genesis)
      └─ HyundaiBlueLinkApiBR (Brazil)
```

### Key Classes

- **VehicleManager** (`VehicleManager.py`): Main entry point. Manages Token lifecycle and Vehicle instances. Factory method `get_implementation_by_region_brand()` selects the appropriate regional API.

- **ApiImpl** (`ApiImpl.py`): Abstract base class defining the interface for all regional implementations.

- **ApiImplType1** (`ApiImplType1.py`): Intermediate class for regions sharing Type 1 protocol (EU, CN, AU, IN).

- **Token** (`Token.py`): Dataclass for authentication state (access_token, refresh_token, valid_until, device_id, pin).

- **Vehicle** (`Vehicle.py`): Dataclass with 100+ properties for vehicle telemetry. Uses private backing fields (`_field`) with public property accessors.

### Adding a New Regional API

1. Create new class extending `ApiImpl` or `ApiImplType1`
2. Implement required methods: `login()`, `get_vehicles()`, `update_vehicle_with_cached_state()`, etc.
3. Register in `VehicleManager.get_implementation_by_region_brand()`
4. Add region constant in `const.py`

### Exception Hierarchy

```python
HyundaiKiaException
├── PINMissingError
├── AuthenticationError
└── APIError
    ├── DeviceIDError
    ├── RateLimitingError
    ├── NoDataFound
    ├── ServiceTemporaryUnavailable
    ├── DuplicateRequestError
    ├── RequestTimeoutError
    └── InvalidAPIResponseError
```

## Project Conventions

- **Python version**: >=3.10
- **Type checking**: Permissive (mypy configured to ignore most errors, pyright disabled)
- **Docstrings**: Minimal; code clarity preferred over extensive documentation
- **pylint**: Many checks disabled globally via file-level directives
- **Constants**: Use enums from `const.py` (REGIONS, BRANDS, ENGINE_TYPES, etc.)
- **Semantic commits**: Required for PRs (enforced by CI)
- **Line length**: 88 characters (Black/flake8 config)

## Testing

Tests are integration tests requiring real credentials via environment variables:
- `KIA_EU_FUATAKGUN_USERNAME`, `KIA_EU_FUATAKGUN_PASSWORD`
- `KIA_CA_CDNNINJA_USERNAME`, `KIA_CA_CDNNINJA_PASSWORD`, `KIA_CA_CDNNINJA_PIN`

Run specific regional tests:
```bash
uv run pytest tests/eu_login_test.py
uv run pytest tests/ca_login_test.py
```

## Important Files

- `const.py`: Region/brand constants, enums for vehicle state
- `exceptions.py`: Custom exception types
- `utils.py`: Helper functions
- `bluelink.py`: CLI entry point (console script)
- `.pre-commit-config.yaml`: Git hooks (ruff, codespell, mypy, pyupgrade)

## API Usage Pattern

```python
from hyundai_kia_connect_api import *

vm = VehicleManager(region=2, brand=1, username="...", password="...", pin="1234")
vm.check_and_refresh_token()
vm.update_all_vehicles_with_cached_state()
print(vm.vehicles)
```

Region/brand IDs are in `const.py`:
- Regions: 1=Europe, 2=Canada, 3=USA, 4=China, 5=Australia, 6=India, 7=NZ, 8=Brazil
- Brands: 1=Kia, 2=Hyundai, 3=Genesis

## Global Python Conventions

Follow instructions from ~/.claude/python.md scrupulously