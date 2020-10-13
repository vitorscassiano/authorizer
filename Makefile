.PHONY: test.unit test.integration test.all

install:
	@pip install -r requirements.txt

test.unit:
	@pytest tests/units

test.integration:
	@pytest tests/integrations

test.all:
	@pytest tests/
