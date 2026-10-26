
from importlib.metadata import version


def test_retailiq_package_is_installed() -> None:
    assert version("retailiq") == "0.1.0"
