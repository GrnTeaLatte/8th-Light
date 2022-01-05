from contextlib import contextmanager
from io import StringIO
import sys
import unittest
from unittest.mock import Mock, mock_open, patch
from requests.exceptions import HTTPError
from app import *

class TestGoogleInterface(unittest.TestCase):
    # testing api validity
    def test_get_google_books_success(self):
        response_json = GoogleInterface.get_google_books('test')
        assert response_json != None
        assert len(response_json['items']) == 5

    #happy path testing
    def test_ok_response_happy_path(self):
        expected_results = {
            'kind': 'books#volumes',
            'totalItems': 2301, 
            'items': [
                {
                    "title": "The Test",
                    "authors": "Sylvian Neuvel",
                    "publisher": "Tor.com",
                },
            ]
        }
        requests = Mock()
        requests.return_value.json = Mock(return_value=expected_results)

        with patch("requests.get", requests):
            results = GoogleInterface.get_google_books('test')

        assert results == expected_results
    
    def test_bad_response_path(self):
        requests = Mock()
        requests.raise_for_status = Mock()
        requests.raise_for_status.side_effect = HTTPError('Google is down')
        
        with patch("requests.get", requests):
            GoogleInterface.get_google_books('test')

        assert self.assertRaises(HTTPError)

class TestLibrary(unittest.TestCase):
    @contextmanager
    def capture_output(self):
        output, error = StringIO(), StringIO()
        old_output, old_error = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = output, error
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_output, old_error

    def test_print_book(self):
        results = [
            {
                "volumeInfo": {
                    "title": "The Test",
                    "authors": ["Sylvian Neuvel"],
                    "publisher": "Tor.com",
                }
            }
        ]

        with self.capture_output() as (out, err):
            Library.print_books(results)
            output = out.getvalue().strip()
            self.assertEqual(output, '1 The Test\n\tAuthor: Sylvian Neuvel\n\tPublisher: Tor.com')
        
    def test_select_options_access(self):
        with self.capture_output() as (out, err):
            with patch('builtins.input', side_effect=[Library.ACCESS_ACTION, Library.BACK_ACTION]):
                Library.select_option([])
                output = out.getvalue().strip()
                self.assertEqual(output, 'Your Reading List is currently empty.')
    
    def test_select_options_bookmark(self):
        with self.capture_output() as (out, err):
            with patch('builtins.input', side_effect=[Library.BOOKMARK_ACTION, Library.BACK_ACTION,  Library.BACK_ACTION]):
                Library.select_option([])
                output = out.getvalue().strip()
                self.assertEqual(output, '')
    
    def test_select_options_invalid_input(self):
        with self.capture_output() as (out, err):
            with patch('builtins.input', side_effect=['Invalid Input', Library.BACK_ACTION]):
                Library.select_option([])
                output = out.getvalue().strip()
                self.assertEqual(output, 'Please enter valid option')

class TestReadingList(unittest.TestCase):
    TEST_BOOK = {
        "id": "3b5uDwAAQBAJ",
        "volumeInfo": {
            "title": "The Test",
            "authors": [
                "Sylvain Neuvel"
            ],
        }
    }

    @contextmanager
    def capture_output(self):
        output, error = StringIO(), StringIO()
        old_output, old_error = sys.stdout, sys.stderr
        try:
            sys.stdout, sys.stderr = output, error
            yield sys.stdout, sys.stderr
        finally:
            sys.stdout, sys.stderr = old_output, old_error

    @contextmanager
    def mock_file_operations(self, file_mock, contents, write_mock):
        with patch('app.open', file_mock, create= True):
            with patch('json.load', contents):
                with patch('json.dump', write_mock):
                    yield

    def test_write(self):
        book_number = 1

        # Mock read and write function to avoid writing test data to sample.json
        file_mock = mock_open()
        contents = Mock()
        contents.side_effect = [ {"reading_list": []} ]
        write_mock = lambda x,y,indent: x

        with self.mock_file_operations(file_mock, contents, write_mock):
            with self.capture_output() as (out, err):
                ReadingList.write(self.TEST_BOOK, book_number)

            output = out.getvalue().strip()
            self.assertEqual(output, "Book 1 saved to Reading List")
        
        file_mock.assert_called_once_with('sample.json', 'r+')

    def test_access_empty_list(self):
        # Mock read and write function to avoid writing test data to sample.json
        file_mock = mock_open()
        contents = Mock()
        contents.side_effect = [ {"reading_list": []} ]
        write_mock = lambda x,y,indent: x
   
        with self.mock_file_operations(file_mock, contents, write_mock):
            with self.capture_output() as (out, err):
                ReadingList.access()

            output = out.getvalue().strip()
            self.assertEqual(output, "Your Reading List is currently empty.")
        
        file_mock.assert_called_once_with('sample.json', 'r')
    
    def test_access_non_empty_list(self):
        # Mock read and write function to avoid writing test data to sample.json
        file_mock = mock_open()
        contents = Mock()
        contents.side_effect = [ {
            "reading_list": [
                self.TEST_BOOK,
            ],
        } ]
        write_mock = lambda x,y,indent: x

        with self.mock_file_operations(file_mock, contents, write_mock):
            with self.capture_output() as (out, err):
                ReadingList.access()
            output = out.getvalue().strip()
            self.assertEqual(output, '1 The Test\n\tAuthor: Sylvain Neuvel\n\tPublisher: n/a')


    
if __name__ == "__main__":
    unittest.main()
