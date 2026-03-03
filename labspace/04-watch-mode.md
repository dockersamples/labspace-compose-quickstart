# Live Development with Watch Mode

Without watch mode, every code change requires you to stop containers, rebuild the image, and restart everything. Docker Compose's **watch mode** automates this loop — syncing your local files into running containers and triggering restarts or rebuilds as needed.

## How watch mode works

The `develop.watch` block defines rules for monitoring file changes:

| Action | What it does |
|--------|-------------|
| `sync` | Copies changed files into the container (no restart) |
| `sync+restart` | Copies changed files and restarts the container process |
| `rebuild` | Rebuilds the image and recreates the container |

For this app:
- **Code changes** (e.g., `app.py`) → `sync+restart` — fast, no full rebuild needed
- **Dependency changes** (`requirements.txt`) → `rebuild` — a new `pip install` is required

## Add the watch configuration

1. Update your Compose file to add the `watch` config:

    ```yaml save-as=compose.yaml highlight=12-20
    services:
      web:
        build: .
        ports:
          - "${APP_PORT:-8000}:5000"
        environment:
          - REDIS_HOST=${REDIS_HOST:-redis}
          - REDIS_PORT=${REDIS_PORT:-6379}
        depends_on:
          redis:
            condition: service_healthy
        develop:
          watch:
            - action: sync+restart
              path: .
              target: /code
              ignore:
                - requirements.txt
            - action: rebuild
              path: requirements.txt

      redis:
        image: redis:alpine
        healthcheck:
          test: ["CMD", "redis-cli", "ping"]
          interval: 5s
          timeout: 5s
          retries: 5
    ```

2. Stop the current containers, then restart with watch mode active:

    ```bash
    docker compose down
    ```

    ```bash terminal-id=watcher
    docker compose up --build --watch
    ```

    The `--watch` flag activates file monitoring. The terminal streams logs and watch events as Compose detects changes.

## Make a live code change

With the watcher running, save an updated version of `app.py` with a different response message:

```python save-as=app.py
import os

from flask import Flask
from redis import Redis

app = Flask(__name__)

redis = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
)


@app.route("/")
def hello():
    count = redis.incr("hits")
    return f"Hello from Docker! You've visited {count} time(s) — keep it up!\n"
```

Watch the `watcher` terminal — Compose detects the change, syncs `app.py` into the running container, and restarts the Flask process automatically.

:tabLink[The page]{href="http://localhost:8000" title="Flask App" id="app"} shows your updated message with no manual rebuild!

> [!NOTE]
> Watch mode is a **development feature** designed for rapid iteration. For production, you'd build a final image with `docker build` and deploy that fixed artifact — not live-synced source code.
