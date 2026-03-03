# Additional commands

## Validate your configuration

```bash
docker compose config
```

This merges all Compose files, resolves `.env` variable substitution, and outputs the final effective configuration. Use it to spot mistakes before they cause runtime errors.

## Stream logs

```bash
docker compose logs -f
```

The `-f` flag follows (tails) the output in real time. Filter to a specific service:

```bash
docker compose logs -f web
```

## Inspect a running container

```bash
docker compose exec redis redis-cli
```

This drops you into an interactive Redis CLI session inside the running `redis` container. Try these commands to inspect the stored data:

```bash no-run-button
KEYS *
GET hits
```

Type `exit` to leave the Redis CLI.
