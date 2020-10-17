.PHONY: help test.install test.check-sec test.unit test.integration test.docker.all test.all test.build build docker.run run
PROJECT_NAME:=authorizer

help:
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST) \
		| tr -d '#'  \
		| awk 'BEGIN {FS = ":.*?@ "}; {printf "\t- \033[36m%-30s\033[0m %s\n", $$1, $$2}'

#test.install: @ Install all dependencies (principal: for the tests)
test.install:
	@pip install -r tests/requirements.txt

#test.check-sec: @ A security linter to verify the code
test.check-sec:
	@echo "checking the security..."
	@bandit -r $(PROJECT_NAME)

#test.unit: @ Runs the unit tests
test.unit:
	@pytest tests/units

#test.integration: @ Runs the integration tests
test.integration:
	@pytest tests/integrations

#test.all: @ Runs every tests (linter tool, unit, integratin)
test.all: | test.check-sec test.unit test.integration

#test.docker.build: @ Builds the docker image for tests
test.docker.build:
	@docker build -t $(PROJECT_NAME)-test -f Dockerfile.test .

#test.docker.all: @ Runs all the tests inside a docker-container
test.docker.all: | test.docker.build
	@docker run -i $(PROJECT_NAME)-test

#build: @ Builds the docker image for the application
build:
	@docker build -t $(PROJECT_NAME) .

#docker.run: @ Runs the application in docker
docker.run: | build
	@docker run -i $(PROJECT_NAME)

#run: @ Runs the application
run:
	@python -m authorizer.app
