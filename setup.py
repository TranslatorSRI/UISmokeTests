"""Setup file for UI Test Runner package."""
from setuptools import setup

with open("README.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="ui-test-runner",
    version="0.0.2",
    author="Max Wang",
    author_email="max@covar.com",
    url="https://github.com/TranslatorSRI/UI_Test_Runner",
    description="Translator UI Test Runner",
    long_description_content_type="text/markdown",
    long_description=readme,
    packages=["ui_test_runner"],
    include_package_data=True,
    install_requires=[
        "jq>=1.6.0",
        "httpx>=0.25.0",
    ],
    zip_safe=False,
    license="MIT",
    python_requires=">=3.9",
)
