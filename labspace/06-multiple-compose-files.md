# Using Multiple Compose files

As applications grow, a single `compose.yaml` becomes harder to maintain. The `include` top-level element lets you split services across multiple files while keeping them part of the same application.

This is especially useful when different teams own different parts of the stack, or when you want to reuse infrastructure definitions across projects.

1. Create a new file in your project called `infra.yaml` and move the Redis service and volume into it:

    ```yaml save-as=infra.yaml
    services:
      redis:
        image: redis:alpine
        volumes:
          - redis-data:/data
        healthcheck:
          test: ["CMD", "redis-cli", "ping"]
          interval: 5s
          timeout: 3s
          retries: 5
          start_period: 10s

    volumes:
      redis-data:
    ```

2. Update `compose.yaml` to include `infra.yaml`:

    ```yaml save-as=compose.yaml
    include:
      - path: ./infra.yaml
    services:
      web:
        build: .
        ports:
          - "${APP_PORT}:5000"
        environment:
          - REDIS_HOST=${REDIS_HOST}
          - REDIS_PORT=${REDIS_PORT}
        depends_on:
          redis:
            condition: service_healthy
        develop:
          watch:
            - action: sync+restart
              path: .
              target: /code
            - action: rebuild
              path: requirements.txt
    ```

3. Run the application to confirm everything still works:

    ```bash
    docker compose up --watch
    ```

    Compose merges both files at startup. The `web` service can still reference `redis` by name because all included services share the same default network.

    This is a simplified example, but it demonstrates the basic principle of `include` and how it can make it easier to modularize complex applications into sub-Compose files. 
    
    For more information on `include` and working with multiple Compose files, see [Working with multiple Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/).

4. Stop the stack before moving on by pressing `Ctrl+C`.