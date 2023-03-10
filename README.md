# Websocket Destination

This is the repository for the Websocket destination connector, written in Python.
For information about how to use this connector within Airbyte, see [the documentation](https://github.com/alexsanderp/hurb-airbyte-connector-destination-websocket).

## Local development

### Prerequisites
**To iterate on this connector, make sure to complete this prerequisites section.**

#### Minimum Python version required `= 3.7.0`

#### [TESTS with WebSocketServer] Minimum NodeJS version required `>= 10.0.0`
```
cd websocket_server/
npm install
```

#### Build & Activate Virtual Environment and install dependencies
From this connector directory, create a virtual environment:
```
python3 -m venv .venv
```

This will generate a virtualenv for this module in `.venv/`. Make sure this venv is active in your
development environment of choice. To activate it from the terminal, run:
```
source .venv/bin/activate
pip install -r requirements.txt
```
If you are in an IDE, follow your IDE's instructions to activate the virtualenv.

Note that while we are installing dependencies from `requirements.txt`, you should only edit `setup.py` for your dependencies. `requirements.txt` is
used for editable installs (`pip install -e`) to pull in Python dependencies from the monorepo and will call `setup.py`.
If this is mumbo jumbo to you, don't worry about it, just put your deps in `setup.py` but install using `pip install -r requirements.txt` and everything
should work as you expect.

#### Create credentials
**If you are a community contributor**, follow the instructions in the [documentation](https://docs.airbyte.com/integrations/destinations/websocket)
to generate the necessary credentials. Then create a file `secrets/config.json` conforming to the `destination_websocket/spec.json` file.
Note that the `secrets` directory is gitignored by default, so there is no danger of accidentally checking in sensitive information.
See `integration_tests/sample_config.json` for a sample config file.

**If you are an Airbyte core member**, copy the credentials in Lastpass under the secret name `destination websocket test creds`
and place them into `secrets/config.json`.

Example:
```json
{
  "websocket_url": "ws://X.X.X.X:9000"
}
```

### Locally running the connector
Run test WebSocketServer to receive data:
```
cd websocket_server/
node websocket_server.js
```

Then run any of the connector commands as follows:
```
python main.py spec
python main.py check --config secrets/config.json
# messages.jsonl is a file containing line-separated JSON representing AirbyteMessages
cat integration_tests/messages.jsonl | python main.py write --config secrets/config.json --catalog integration_tests/configured_catalog.json
```

### Locally running the connector docker image

#### Build
First, make sure you build the latest Docker image:
```
docker build . -t airbyte/destination-websocket:dev
```

#### Run
Run test WebSocketServer to receive data:
```
cd websocket_server/
node websocket_server.js
```

Then run any of the connector commands as follows:
```
docker run --rm airbyte/destination-websocket:dev spec
docker run --rm -v $(pwd)/secrets:/secrets airbyte/destination-websocket:dev check --config /secrets/config.json
# messages.jsonl is a file containing line-separated JSON representing AirbyteMessages
cat integration_tests/messages.jsonl | docker run -i --rm -v $(pwd)/secrets:/secrets -v $(pwd)/integration_tests:/integration_tests airbyte/destination-websocket:dev write --config /secrets/config.json --catalog /integration_tests/configured_catalog.json
```

### Locally using the connector in Airbyte (minikube)

#### Prerequisites
See https://github.com/alexsanderp/hurb-airbyte to run local airbyte in minikube.

#### Build
```
docker build -t airbyte/destination-websocket:dev .
```

#### Using
Run test WebSocketServer to receive data:
```
cd websocket_server/
node websocket_server.js
```

Send docker image to minikube:
```
minikube image load airbyte/destination-websocket:dev
```

Go to airbyte url: http://localhost:8000

Go to Settings > Destinations
![img.png](images/1.png)

Click in New connector and register the docker image
![img.png](images/2.png)

Now create a new destination with the websocket url of your WebSocketServer (ws://YOUR_MACHINE'S_IP:9000)

Create a pipeline using any source and the new registered destination to test :)

WebSocketServer output:
![img.png](images/3.png)

## Testing
   Make sure to familiarize yourself with [pytest test discovery](https://docs.pytest.org/en/latest/goodpractices.html#test-discovery) to know how your test files and methods should be named.
First install test dependencies into your virtual environment:
```
pip install .[tests]
```
### Unit Tests
To run unit tests locally, from the connector directory run:
```
python -m pytest unit_tests
```

### Integration Tests
There are two types of integration tests: Acceptance Tests (Airbyte's test suite for all destination connectors) and custom integration tests (which are specific to this connector).
#### Custom Integration tests
Place custom tests inside `integration_tests/` folder, then, from the connector root, run
```
python -m pytest integration_tests
```

## Dependency Management
All of your dependencies should go in `setup.py`, NOT `requirements.txt`. The requirements file is only used to connect internal Airbyte dependencies in the monorepo for local development.
We split dependencies between two groups, dependencies that are:
* required for your connector to work need to go to `MAIN_REQUIREMENTS` list.
* required for the testing need to go to `TEST_REQUIREMENTS` list
