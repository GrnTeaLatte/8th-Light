import requests
import json
import urllib.parse

EXIT_ACTION = 'E'

class GoogleInterface():    
    GOOGLE_QUERY_URL = 'https://www.googleapis.com/books/v1/volumes?q='

    def get_google_books(query):
        parameters = {
            "maxResults" : 5,
            "printType" : "books"
        }
        try:
            response = requests.get(
                f"{GoogleInterface.GOOGLE_QUERY_URL}{query}", params = parameters
            )
            response.raise_for_status()
        except Exception as e:
            print(e)

        return response.json()

class Library():
    ACCESS_ACTION = 'access'
    BOOKMARK_ACTION = 'bookmark'
    BACK_ACTION = 'back'

    def print_books(results):
        for index, item in enumerate(results):
            book_info = item['volumeInfo']
            title = book_info.get('title', "n/a") 
            author = ', '.join(book_info.get('authors', "")) or 'n/a'
            publisher = book_info.get('publisher', "n/a")
            
            print(index+1, f"{title}\n\tAuthor: {author}\n\tPublisher: {publisher}") 
            
    def select_option(results):
        option = input(f"Type '{Library.BOOKMARK_ACTION}' to save book(s) to Reading List, '{Library.ACCESS_ACTION}' to view Reading List or '{Library.BACK_ACTION}' to go back to search: ")
        option = option.lower()
        while option != Library.BACK_ACTION:          
            if option == Library.BOOKMARK_ACTION:     
                Library.write_reading_list(results)
            elif option == Library.ACCESS_ACTION:    
                ReadingList.access()
            else:
                print("Please enter valid option")

            option = input(f"Type '{Library.BOOKMARK_ACTION}' to save book(s) to Reading List, '{Library.ACCESS_ACTION}' to view Reading List or '{Library.BACK_ACTION}' to go back to search: ")
            option = option.lower()

    def write_reading_list(results):
        option = input(f"Type the number to bookmark to Reading List or '{Library.BACK_ACTION}' to go back to options: ")
        option = option.lower()
        while option != Library.BACK_ACTION:
            if option.isdigit():    
                book_number = int(option)

                if book_number in range(1,6):   
                    book = results['items'][book_number-1]

                    ReadingList.write(book, book_number)
                else:
                    print('Please enter a valid number between 1 and 5')
            else:
                print('Please enter a valid number between 1 and 5')

            option = input(f"Type the number to bookmark to Reading List or '{Library.BACK_ACTION}' to go back to options: ")
            option = option.lower()

class ReadingList():
    def write(book, book_number):
        with open("sample.json", "r+") as file: # writing and appending to json file
            file_data = json.load(file)
            if any(saved_book['id'] == book['id'] for saved_book in file_data["reading_list"]): # if book already exists on List, do not add
                print(f"Book {book_number} is already on the Reading List")
            else:
                file_data["reading_list"].append(book)     
                file.seek(0)
                json.dump(file_data, file, indent = 4)

                print(f"Book {book_number} saved to Reading List\n")

    def access():  
        with open('sample.json', 'r') as file:
            file_data = json.load(file)
            if len(file_data['reading_list']) == 0:     
                print("Your Reading List is currently empty.")
            else:
                Library.print_books(file_data['reading_list'])  

# sanitize query in case user enters harmful characters
def sanitize_query(query):
    sanitized_query = urllib.parse.quote(query.strip()) 
    return sanitized_query

#handle empty inputs
def is_valid_query(query):
    return len(query) > 0 

def run_program():
    # User search google books
    user_input = input(f"Find Books by Title or type '{EXIT_ACTION}' to Exit: ") 
    while user_input != EXIT_ACTION: 
        query = sanitize_query(user_input) 
        if is_valid_query(query):
            results = GoogleInterface.get_google_books(query)   
            if results['totalItems'] != 0:      # if the search returns valid results, display first 5 results 
                Library.print_books(results['items'])
                Library.select_option(results)          # allow user to add to Reading List, perform another search, or view list
            else:
                print('No results found, please try again.')    
        else:
            print('Please enter valid search term')
        user_input = input(f"Find Books by Title or type '{EXIT_ACTION}' to Exit: ")

run_program()