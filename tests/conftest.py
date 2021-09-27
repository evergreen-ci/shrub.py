"""Test configuration."""
import json
import os
from pathlib import Path

import pytest
import yaml

TESTS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DATA_PATH = os.path.join(TESTS_DIRECTORY, "integration", "data")


def read_test_data_file(filename):
    with open(os.path.join(SAMPLE_DATA_PATH, filename)) as f:
        return f.read()


def compare_format(expected_file, actual, format_fn):
    expected = read_test_data_file(expected_file)

    expected_formatted = format_fn(expected)
    actual_formatted = format_fn(actual)

    assert expected_formatted == actual_formatted


@pytest.fixture()
def compare_json():
    return lambda filename, actual: compare_format(filename, actual, json.loads)


@pytest.fixture()
def compare_yaml():
    return lambda filename, actual: compare_format(filename, actual, yaml.safe_load)


@pytest.fixture()
def sample_files_location():
    return Path(SAMPLE_DATA_PATH)
