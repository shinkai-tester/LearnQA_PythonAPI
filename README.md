# LearnQA_PythonAPI

## What is used:
- Application: https://playground.learnqa.ru/api/map
- Python 3.9.7 ([click](https://www.python.org/downloads/) to download the current python version)
- [pytest](https://docs.pytest.org/en/latest/getting-started.html#), [requests HTTP lib](https://docs.python-requests.org/en/latest/), [allure](https://docs.qameta.io/allure/#_pytest) -> please see ***requirements.txt***

Use command in PyCharm -> Terminal under the project path:
```
pip3 install -r requirements.txt
```
## Run the tests
To run the tests from the terminal under the project path, use the following command:
```
python -m pytest -s --alluredir=test_results/ tests/
```
## Allure report
To generate the report, use the command:
```
allure serve test_results
```
