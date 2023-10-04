"""Setup file for UI Test Runner package."""
from setuptools import setup

setup(
    name="ui-test-runner",
    version="0.0.1",
    author="CoVar",
    url="https://github.com/TranslatorSRI/UI_Test_Runner",
    description="Translator UI Test Runner",
    packages=["ui_test_runner"],
    include_package_data=True,
    zip_safe=False,
    license="MIT",
    python_requires=">=3.9",
)
