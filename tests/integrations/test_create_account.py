import json
import contextlib

from io import StringIO
from unittest import TestCase, skip
from unittest.mock import patch
from authorizer.app import main


class TestAccountService(TestCase):
    def setUp(self):
        self.mock_stdout = StringIO()

    def test_should_create_account(self):
        operation = {"account": {"activeCard": True, "availableLimit": 100}}
        mock_stdin = StringIO(json.dumps(operation))
        with contextlib.redirect_stdout(self.mock_stdout):
            with patch("sys.stdin", mock_stdin) as _:
                main()

        expected = {
            "account": {
                "activeCard": True,
                "availableLimit": 100,
                "violations": []
            }
        }
        result = json.loads(self.mock_stdout.getvalue().rstrip())
        self.assertDictEqual(expected, result)

    def test_should_not_create_already_initialized_account(self):
        operation = map(lambda j: json.dumps(j), [
            {"account": {"activeCard": True, "availableLimit": 100}},
            {"account": {"activeCard": True, "availableLimit": 100}}
        ])
        mock_stdin = StringIO("\n".join(operation))

        with contextlib.redirect_stdout(self.mock_stdout):
            with patch("sys.stdin", mock_stdin) as _:
                main()

        expected = [{
            "account": {
                "activeCard": True,
                "availableLimit": 100,
                "violations": []
            }
        }, {
            "account": {
                "activeCard": True,
                "availableLimit": 100,
                "violations": ["account-already-initialized"]
            }
        }]
        result = [json.loads(j) \
            for j in self.mock_stdout.getvalue().rstrip().split("\n")]
        self.assertEqual(expected, result)

    @skip("under development")
    def test_should_raise_account_not_found(self): pass
