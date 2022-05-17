import pytest
from click.testing import CliRunner
from pandas_cli.main import cli


def test_load():
    runner = CliRunner()
    res = runner.invoke(cli, ["load"])
