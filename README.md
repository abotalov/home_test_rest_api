# Home test REST API

This repository contains test cases for [PoetryDb](https://github.com/thundercomb/poetrydb).

## Test Cases

| Test Case name             | Endpoint                | Expected Result                                          |
|----------------------------|-------------------------|----------------------------------------------------------|
| TestAuthor                 | /author/:author	        | The API returns poems authored by the expected author.   |
| TestTitle                  | /title/:title           | The API returns poems titled the expected title.         |
| TestLines                  | /lines/:line            | The API returns poems containing the specified line.     |
| TestLineCount              | /linecount/:count       | The API returns poems with the specifed number of lines. |
| TestPoemCount              | /poemcount/:count       | The API returns the specified number of poems.           |
| TestErrorInvalidEndpoint   | /invalidendpoint/:value | The API returns a 405 error.                             |
| TestErrorInvalidSearchTerm | /author/:invalid        | The API returns a 404 error.                             |

Also:
* all test cases have a validation that status code is 200
* successful test cases have validations that response is a non-empty JSON array and it contains the expected fields.

The validations were chosen to comprehensively verify:
* API Status Code
* Response Structure and fields
* Content correctness
* Error handling

Pytest `assert`s were used for validation for the following reasons:
* Short natural language syntax without boilerplate
* Informative failure messages due to pytest introspection

## Running the tests

### Option 1 - Locally

1. Install dependencies, e.g.
```
pip install -r requirements.txt
```

3. Run the tests:
```
pytest
```

### Option 2 - In Docker

1. Build the Docker image:
```
docker build -t home-test-rest-api .
```

2. Run the tests:
```
docker run --rm home-test-rest-api
```
