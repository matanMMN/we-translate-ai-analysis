import sys
import pytest


pytestmark = pytest.mark.anyio

TEST_PATH = None

ARGS = [
    "-qq", # quiet
    # "--show-capture=no" # captured caplog
    # "--maxfail=1", # max fails
    "-rA", # show summary of tests
    "-v", # verbose
    "--tb=long", # traceback
    "-x", # stops after first failure
    # "--disable-warnings"
    # "--k controller",

]
if TEST_PATH is not None:
    ARGS.append(
        f"-q ${TEST_PATH}"
    )

PLUGINS = [
    # "logging-plugin"
]


if __name__ == "__main__":
    sys.exit(pytest.main(ARGS, plugins=PLUGINS))
