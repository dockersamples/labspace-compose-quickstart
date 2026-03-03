# Persistence & Debugging

Your hit counter still resets to zero when containers are removed. That's because Redis stores data in its container's writable layer — and that layer disappears with `docker compose down`. **Named volumes** solve this by storing data outside the container lifecycle, on the Docker host itself.

## Add a named volume

1. Update your Compose file to mount a named volume into Redis's data directory, and add a `volumes` section at the top level to declare it:

    ```yaml save-as=compose.yaml highlight=29-33
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
        volumes:
          - redis-data:/data

    volumes:
      redis-data:
    ```

2. Stop any running containers, then start fresh:

    ```bash
    docker compose down
    ```

    ```bash
    docker compose up --build -d
    ```

3. Visit :tabLink[the Flask App]{href="http://localhost:8000" title="Flask App" id="app"} and refresh several times to build up a count:

4. Now stop the containers — but notice this time the `redis-data` volume is **not** removed:

    ```bash
    docker compose down
    ```

5. Bring everything back up:

    ```bash
    docker compose up -d
    ```

6. Visit :tabLink[the Flask App]{href="http://localhost:8000" title="Flask App" id="app"} again.

    The counter picks up exactly where it left off! The `redis-data` volume persists independently of the container lifecycle.

> [!TIP]
> To also delete volumes when tearing down, use `docker compose down -v`. This is useful when you want a completely clean slate during development.
