# Health Checks & Startup Order

Right now, your `web` service starts at roughly the same time as `redis`. But what if Redis isn't ready to accept connections when Flask first tries to connect? The `web` container crashes before it can serve a single request.

This is a **startup race condition**, and it's a common issue in multi-container applications.

## The solution: healthcheck + depends_on

Docker Compose can wait for one service to become *healthy* before starting another. You need two things:

1. A **healthcheck** on `redis` that actively tests whether it's ready to accept connections
2. A `depends_on` condition on `web` that waits until `redis` is healthy

Update your Compose file to add both the `depends_on` and `healthcheck` configurations:

```yaml save-as=compose.yaml highlight=9-11,15-19
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

  redis:
    image: redis:alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5
```

The healthcheck runs `redis-cli ping` every 5 seconds. Once Redis responds with `PONG`, it's considered healthy — and only then will `web` start.

## See it in action

1. Start the application:

    ```bash
    docker compose up --build -d
    ```

2. Watch the startup sequence:

    ```bash
    docker compose ps
    ```

    The `redis` service will show `(healthy)` in its status before `web` finishes starting. This guarantees correct startup order every time, regardless of machine speed.

3. Visit the app to confirm everything is working by going to :tabLink[http://localhost:8000]{href="http://localhost:8000" title="Flask App" id="app"}

> [!TIP]
> The `depends_on` field supports three conditions:
>
> - `service_started` — the container has been created (the default)
> - `service_healthy` — the container's healthcheck is passing
> - `service_completed_successfully` — the container exited with code 0 (useful for database migration init containers)
