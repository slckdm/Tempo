# Tempo Toolkit

Shared Python code for Tempo is distributed as three independently installable wheels with a
single `tempo_toolkit` namespace:

- `tempo-toolkit-contracts` contains stable identifiers, upload types, events, and routing keys.
- `tempo-toolkit-application` contains framework-independent ports, services, errors, and the
  transactional outbox model.
- `tempo-toolkit-infrastructure` contains FastAPI, Keycloak, Redis, PostgreSQL/SQLAlchemy, S3, and
  RabbitMQ integrations.

Dependencies must only point in this direction:

```text
contracts <- application <- infrastructure
```

## Development

```bash
uv sync --all-packages --all-extras
make check
make build
```

The three packages use the same release version. `make publish` builds them and publishes them to
the local pypiroska index in dependency order.

Services use editable path dependencies during host development and select only the required
infrastructure extras. Docker builds use the three corresponding wheels from pypiroska.

