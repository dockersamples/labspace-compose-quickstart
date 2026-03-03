# Welcome to Docker Compose Quickstart! 🐳

Docker Compose is a tool for defining and running multi-container applications. Instead of managing each container by hand, you describe your entire application stack in a single `compose.yaml` file and bring everything up with one command.

In this lab, you'll build a **Python Flask web app** backed by **Redis** — a classic multi-container setup. Along the way, you'll learn how to:

- Define services in a `compose.yaml` file
- Control startup order with health checks
- Iterate on code quickly with watch mode
- Persist data across container restarts

## Verify your environment

Before diving in, confirm that Docker and Compose are available:

```bash
docker version
```

```bash
docker compose version
```

You should see version information for both. If either command fails, the environment may need a moment to initialize — try again in a few seconds.

## Tour the starter files

The project already contains everything needed to build and run the app. Take a look:

```bash
ls -la
```

| File | Purpose |
|------|---------|
| `app.py` | The Flask web application |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Instructions to build the container image |
| `.env` | Default environment variable values |
| `.dockerignore` | Files to exclude from the build context |

Open :fileLink[app.py]{path="app.py"} to see the application code. It's a simple hit counter that increments a value in Redis each time someone visits the page, and reports the total back to the browser.

Open :fileLink[Dockerfile]{path="Dockerfile"} to see how the image is built. It starts from the official `python:3.12-alpine` base, installs dependencies, copies the source code, and runs Flask.

> [!NOTE]
> Notice that `.env` is listed in `.dockerignore`. This prevents the `.env` file from being copied into the container image during `docker build` — a good security practice, since `.env` files often contain secrets.

In the next section, you'll connect these pieces together using Docker Compose.
