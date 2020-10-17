import json
import contextlib

from io import StringIO
from unittest import TestCase, skip
from unittest.mock import patch
from authorizer.app import main


def test_sould_create_account():
    mock_stdout = StringIO()
    operations = {"account": {"activeCard": True, "availableLimit": 100}}
    mock_stdin = StringIO(json.dumps(operations))

    with contextlib.redirect_stdout(mock_stdout):
        with patch("sys.stdin", mock_stdin) as _:
            main()

    expected = {
        "account": {
            "activeCard": True,
            "availableLimit": 100,
            "violations": []
        }
    }
    stdout = json.loads(mock_stdout.getvalue().rstrip())
    assert stdout == expected

def test_should_not_create_already_initialized_account():
    mock_stdout = StringIO()
    operations = map(lambda j: json.dumps(j), [
        {"account": {"activeCard": True, "availableLimit": 100}},
        {"account": {"activeCard": True, "availableLimit": 100}}
    ])
    mock_stdin = StringIO("\n".join(operations))

    with contextlib.redirect_stdout(mock_stdout):
        with patch("sys.stdin", mock_stdin) as _:
            main()

    expected = [
        {"account": {"activeCard": True, "availableLimit": 100, "violations": []}},
        {"account": {"activeCard": True, "availableLimit": 100,
                     "violations": ["account-already-initialized"]}}
    ]

    stdout = [json.loads(j)
              for j in mock_stdout.getvalue().rstrip().split("\n")]

    assert stdout == expected