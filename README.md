# Authorizer Challanger
The application that authorizes a transaction for a specific account following a set of predefined rules.

Predefined rules:
- account-already-initialized
- insufficient-limit
- card-not-active
- high-frequency-small-interval
- doubled-transaction

#### Requirements
- [Python 3.8+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started) (Optional)


### TLDR
#### Available targets
```shell
> make help
	- test.install                   Install all dependencies (principal: for the tests)
	- test.check-sec                 A security linter to verify the code
	- test.unit                      Runs the unit tests
	- test.integration               Runs the integration tests
	- test.all                       Runs every tests (linter tool, unit, integratin)
	- test.docker.build              Builds the docker image for tests
	- test.docker.all                Runs all the tests inside a docker-container
	- build                          Builds the docker image for the application
	- docker.run                     Runs the application in docker
	- run                            Runs the application
```

## Installing the dependencies

You can install all the dependencies running the following command:
```shell
> make test.install
```
> These dependencies are required for the test scope, you could not install dependencies if no needs.

## Running the tests
There is two available environments for running tests:

#### System
You could run these tests running the following command:
```shell
> make test.all
```

#### Docker
You could run these tests running the following command:
```shell
> make test.docker.all
```

## Running the application
For running the application as streaming you can use the input redirection operator `<` or passing the stdin as required.\
The followinng example use this operator:

#### System
```shell
> python -m authorizer.app < operations
```

#### Docker
```shell
> make run < operations
```
