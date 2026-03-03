# Labspace - Compose Quickstart

An interactive lab that teaches Docker Compose fundamentals by building a multi-container Python Flask and Redis application from scratch. Learners progress from a bare `compose.yaml` through health checks, live development with watch mode, data persistence with volumes, and multi-file Compose configurations.

## Learning objectives

This Labspace will teach you the following:

- Define a multi-service app in a `compose.yaml` file
- Control startup order with health checks and `depends_on`
- Iterate on code quickly using watch mode
- Persist data across container restarts with named volumes
- Compose multi-file configurations with the `include` directive
- Use core debugging commands (`config`, `logs`, `exec`)

## Launch the Labspace

To launch the Labspace, run the following command:

```bash
docker compose -f oci://dockersamples/labspace-compose-quickstart up -d
```

And then open your browser to http://localhost:3030.

### Using the Docker Desktop extension

If you have the Labspace extension installed (`docker extension install dockersamples/labspace-extension` if not), you can also [click this link](https://open.docker.com/dashboard/extension-tab?extensionId=dockersamples/labspace-extension&location=dockersamples/labspace-compose-quickstart&title=Compose%20Quickstart) to launch the Labspace.

## Contributing

If you find something wrong or something that needs to be updated, feel free to submit a PR. If you want to make a larger change, feel free to fork the repo into your own repository.

**Important note:** If you fork it, you will need to update the GHA workflow to point to your own Hub repo.

1. Clone this repo

2. Start the Labspace in content development mode:

    ```bash
    # On Mac/Linux
    CONTENT_PATH=$PWD docker compose up --watch

    # On Windows with PowerShell
    $Env:CONTENT_PATH = (Get-Location).Path; docker compose up --watch
    ```

3. Open the Labspace at http://dockerlabs.xyz.

4. Make the necessary changes and validate they appear as you expect in the Labspace

    Be sure to check out the [docs](https://github.com/dockersamples/labspace-infra/tree/main/docs) for additional information and guidelines.
