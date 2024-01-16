# review_classification

This is a [Dagster](https://dagster.io/) project demonstrating how to build a
production quality ML pipeline in Python. Please read the rest of this README to
understand how the different parts of this solution work.

## Getting started

First, create a new virtual environment in the directory where you cloned the
repository.

```bash
python -m venv .venv
pip install --upgrade pip setuptools poetry
```

Next, install the package itself:

```bash
poetry install
```

Then, start the Dagster UI web server:

```bash
dagster dev
```

Open http://localhost:3000 with your browser to see the project.

You can start writing assets in `review_classification/assets.py`. The assets
are automatically loaded into the Dagster code location as you define them.

## Development

### Adding new Python dependencies

You can use `poetry add <package>` to install new packages in the project.

### Unit testing

Tests are in the `tests` directory and you can run tests using `pytest`:

```bash
pytest tests
```

### Schedules and sensors

If you want to enable Dagster
[Schedules](https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules)
or
[Sensors](https://docs.dagster.io/concepts/partitions-schedules-sensors/sensors)
for your jobs, the
[Dagster Daemon](https://docs.dagster.io/deployment/dagster-daemon) process must
be running. This is done automatically when you run `dagster dev`.

Once your Dagster Daemon is running, you can start turning on schedules and
sensors for your jobs.
