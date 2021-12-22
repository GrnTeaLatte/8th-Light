import requests 
import json
import urllib.parse

ACCESS_ACTION = 'access'
BOOKMARK_ACTION = 'bookmark'
BACK_ACTION = 'back'
EXIT_ACTION = 'E'

GOOGLE_QUERY_URL = 'https://www.googleapis.com/books/v1/volumes?q='

# API calls to google books
def get_google_books(query):
    # Limit 5 results, search only books
    parameters = {
        "maxResults" : 5,
        "printType" : "books"
    }
    try:
        response = requests.get(
            f"{GOOGLE_QUERY_URL}{query}", params = parameters
        )
        response.raise_for_status()
    # error handling
    except Exception as e:
        print(e)

    return response.json()

# json parse results for title, author(s) and publisher, n/a to handle missing data
def print_books(results):
    for index, item in enumerate(results):
        book_info = item['volumeInfo']
        title = book_info.get('title', "n/a") 
        author = ', '.join(book_info.get('authors', "")) or 'n/a'
        publisher = book_info.get('publisher', "n/a")
         
        print(index+1, f"{title}\n\tAuthor: {author}\n\tPublisher: {publisher}") #print with index
        
# options for user to use different aspects of application
def select_option(results):
    option = input(f"Type '{BOOKMARK_ACTION}' to save book(s) to Reading List, '{ACCESS_ACTION}' to view Reading List or '{BACK_ACTION}' to go back to search: ")
    option = option.lower()
    while option != BACK_ACTION:         # 'back' to do another search or exit 
        if option == BOOKMARK_ACTION:     # 'Bookmark' to save to Reading List
            write_reading_list(results)
        elif option == ACCESS_ACTION:    # 'Access' to view Reading List
            access_reading_list()
        else:
            print("Please enter valid option")

        option = input(f"Type '{BOOKMARK_ACTION}' to save book(s) to Reading List, '{ACCESS_ACTION}' to view Reading List or '{BACK_ACTION}' to go back to search: ")
        option = option.lower()

# Writing to Reading List
def write_reading_list(results):
    option = input(f"Type the number to bookmark to Reading List or '{BACK_ACTION}' to go back to options: ")
    option = option.lower()
    while option != BACK_ACTION:
        if option.isdigit():    # allowing only number submissions
            book_number = int(option)

            if book_number in range(1,6):   # only numbers 1-5
                book = results['items'][book_number-1]

                with open("sample.json", "r+") as file: # writing and appending to json file
                    file_data = json.load(file)
                    if any(saved_book['id'] == book['id'] for saved_book in file_data["reading_list"]): # if book already exists on List, do not add
                        print(f"Book {book_number} is already on the Reading List")
                    else:
                        file_data["reading_list"].append(book) # adding book to Reading List as list    
                        file.seek(0)
                        json.dump(file_data, file, indent = 4)

                        print(f"Book {book_number} saved to Reading List\n")
            else:
                print('Please enter a valid number between 1 and 5')
        else:
            print('Please enter a valid number between 1 and 5')

        option = input(f"Type the number to bookmark to Reading List or '{BACK_ACTION}' to go back to options: ")
        option = option.lower()

# Viewing the Reading List
def access_reading_list():  
    with open('sample.json', 'r') as file:
        file_data = json.load(file)
        if len(file_data['reading_list']) == 0:     # checking if reading list is empty
            print("Your Reading List is currently empty.")
        else:
            print_books(file_data['reading_list'])  

# sanitize query in case user enters harmful characters
def sanitize_query(query):
    sanitized_query = urllib.parse.quote(query.strip()) 
    return sanitized_query

#handle empty inputs
def is_valid_query(query):
    return len(query) > 0 

# Running the application
def run_program():
    user_input = input(f"Find Books by Title or type '{EXIT_ACTION}' to Exit: ") # User search google books
    while user_input != EXIT_ACTION: 
        query = sanitize_query(user_input)  # sanitizing query and making sure it's valid 
        if is_valid_query(query):
            results = get_google_books(query)   # getting json results through API call
            if results['totalItems'] != 0:      # if the search returns valid results, display first 5 results 
                print_books(results['items'])
                select_option(results)          # allow user to add to Reading List, perform another search, or view list
            else:
                print('No results found, please try again.')    
        else:
            print('Please enter valid search term')
        user_input = input(f"Find Books by Title or type '{EXIT_ACTION}' to Exit: ")

run_program()