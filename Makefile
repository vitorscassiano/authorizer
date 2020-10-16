.PHONY: test.unit test.integration test.all test.build build run
PROJECT_NAME:=authorize

test.install:
	@pip install -r tests/requirements.txt

test.unit:
	@pytest tests/units

test.integration:
	@pytest tests/integrations

test.all: | test.build
	@docker run $(PROJECT_NAME)-test

test.build:
	@docker build -t $(PROJECT_NAME)-test -f Dockerfile.test .

build:
	@docker build -t $(PROJECT_NAME) .

run:
	@docker run -i $(PROJECT_NAME)
