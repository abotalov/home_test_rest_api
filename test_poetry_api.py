from urllib import parse

import pytest
import requests

BASE_URL = "https://poetrydb.org"


class BaseTestPoetryApi:
    """Base class for testing the PoetryDB API."""

    @pytest.fixture(scope="class")
    def url(self, request):
        """Returns URL of the endpoint."""
        input_field_endpoint = request.cls.input_field_endpoint
        search_term = request.cls.search_term
        return f"{BASE_URL}/{input_field_endpoint}/{parse.quote(search_term)}"

    @pytest.fixture(scope="class")
    def response(self, url):
        """Fixture to send a GET request to the specified endpoint with the given value."""
        return requests.get(url)

    @pytest.fixture(scope="class")
    def json_data(self, response):
        """Fixture to send a GET request to the specified endpoint with the given value."""
        return response.json()

    def test_status_code(self, response):
        """Validates that status code is 200."""
        assert response.status_code == 200


class BaseTestSuccessfulResponse(BaseTestPoetryApi):
    """Base class for tests expecting a successful response."""

    def test_response_is_json_array(self, json_data):
        """Validates that the response is a non-empty JSON array."""
        assert isinstance(json_data, list)
        assert len(json_data) > 0

    def test_poem_fields(self, json_data):
        """Validates that each poem contains the expected fields."""
        expected_fields = {"title", "author", "lines", "linecount"}
        for poem in json_data:
            assert expected_fields.issubset(poem.keys())


class TestAuthor(BaseTestSuccessfulResponse):
    """
    Test case for retrieving poems by the author.
    Endpoint: /author/Mark%20Twain
    """

    input_field_endpoint = "author"
    search_term = "Mark Twain"

    def test_poem_matches_author(self, json_data):
        for poem in json_data:
            assert poem["author"] == self.search_term


class TestTitle(BaseTestSuccessfulResponse):
    """
    Test case for retrieving poems by the title.
    Endpoint: /title/A%20Sweltering%20Day%20In%20Australia
    """

    input_field_endpoint = "title"
    search_term = "A Sweltering Day In Australia"

    def test_poem_matches_title(self, json_data):
        for poem in json_data:
            assert poem["title"] == self.search_term


class TestLines(BaseTestSuccessfulResponse):
    """
    Test case for retrieving poems containing specific lines.
    Endpoint: /lines/one%20swift
    """

    input_field_endpoint = "lines"
    search_term = "one swift"

    def test_poem_contains_line(self, json_data):
        search_term = self.search_term.lower()
        for poem in json_data:
            assert [line for line in poem["lines"] if search_term in line.lower()]


class TestLineCount(BaseTestSuccessfulResponse):
    """
    Test case for retrieving poems containing specified linecount.
    Endpoint: /linecount/80
    """

    input_field_endpoint = "linecount"
    search_term = "80"

    def test_poem_linecount(self, json_data):
        for poem in json_data:
            assert poem["linecount"] == self.search_term
            non_empty_lines = [line for line in poem["lines"] if line != ""]
            assert len(non_empty_lines) == int(self.search_term)


class TestPoemCount(BaseTestSuccessfulResponse):
    """
    Test case for retrieving specified number of poems.
    Endpoint: /poemcount/7
    """

    input_field_endpoint = "poemcount"
    search_term = "7"

    def test_poem_count(self, json_data):
        assert len(json_data) == int(self.search_term)


class TestErrorInvalidEndpoint(BaseTestPoetryApi):
    """
    Test case for querying an invalid endpoint.
    Endpoint: /invalidendpoint/test
    """

    input_field_endpoint = "invalidendpoint"
    search_term = "test"

    def test_error_message(self, json_data):
        assert json_data["status"] == "405"
        assert "input field not available" in json_data["reason"]


class TestErrorInvalidSearchTerm(BaseTestPoetryApi):
    """
    Test case for querying an invalid search term.
    Endpoint: /author/NonExistentAuthor
    """

    input_field_endpoint = "author"
    search_term = "NonExistentAuthor"

    def test_error_message(self, json_data):
        assert json_data["status"] == 404
        assert json_data["reason"] == "Not found"
