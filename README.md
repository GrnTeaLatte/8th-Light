This command line application takes in a request from the user for a book search on Google Books, and returns the first five most relevent results. The user is then allowed to save a book from the search to a local Reading List, and then have the ability to view that reading list at a later time.

The program makes API calls from Google Books, then parses the json responses to only include the title, author(s) and publisher of the volume.

This program is written in python.

To get started, first download a recent installation of the Python interpreter(https://www.python.org/downloads/).

Install requests (REST API framework)
```
$ pip install -U requests
```

Run the program from a terminal:
```
$ python3 app.py
```

Problem Description

Code Submission
Create a command line application that allows you to use the Google Books API to search for books and construct a reading list.

You do not have to use a private GitHub repo for this.

This application should allow you to:

    Type in a query and display a list of 5 books matching that query.
    Each item in the list should include the book's author, title, and publishing company.
    A user should be able to select a book from the five displayed to save to a “Reading List”
    View a “Reading List” with all the books the user has selected from their queries -- this is a local reading list and not tied to Google Books’s account features.

For programming language, choose any language you want as long as it is not the same language you chose to review in the Code Review section above. Feel free to use a library (or not) for the Google Books call or JSON parsing.

Please do not add any additional features.

Your submission doesn’t need to be perfect. After we receive your submission we'll review your code, respond to you with our feedback and suggestions, and give you an opportunity to respond to our feedback and make improvements to your code before you re-submit a second and final version.

That said, we would still like to see your best work with the first version you submit. It should demonstrate external quality (for example: solves the problem, handles edge cases, usability), internal quality (for example: decoupling, testing, readability), as well as some idea of your process and approach (via your version control history and README).

To submit your work, please complete this form: https://app3.greenhouse.io/application_form/150000a6305cca3cc3898f4bc5c08e0c?utm_medium=email&utm_source=FormMailer%23form_email&utm_source=EmailForm
