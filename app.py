import requests 
import json
 
def get_google_books(query):
    parameters = {
        "maxResults" : 5
    }
    try:
        response = requests.get(
            f"https://www.googleapis.com/books/v1/volumes?q={query}", params = parameters
        )
        response.raise_for_status()
    # error handling
    except Exception as e:
        print(e)

    return response.json()

def print_books(results):
    for index, item in enumerate(results):
        book_info = item['volumeInfo']
        title = book_info.get('title', "n/a")
        author = ', '.join(book_info.get('authors', "")) or 'n/a'
        publisher = book_info.get('publisher', "n/a")
         
        print(index+1, f"{title}\n\tAuthor: {author}\n\tPublisher: {publisher}")
        
def select_option(results):
    option = input("Type 'Bookmark' to save book(s) to Readling List, 'Access' to view Reading List or 'back' to go back to search: ")
    while option != 'back':
        if option =='Bookmark':
            write_reading_list(results)
        elif option == 'Access':
            access_reading_list()
        else:
            print("Please enter valid option")

        option = input("Type 'Bookmark' to save book(s) to Readling List, 'Access' to view Reading List or 'back' to go back to search: ")

def write_reading_list(results):
    option = input("Type Number to bookmark to Reading List or 'back' to go back to options: ")
    while option != "back":
        if option.isdigit():
            book_number = int(option)

            if book_number in range(1,6):
                book = results['items'][book_number-1]

                with open("sample.json", "r+") as file:
                    file_data = json.load(file)
                    if any(saved_book['id'] == book['id'] for saved_book in file_data["reading_list"]):
                        print(f"Book {book_number} is already on the Reading List")
                    else:
                        file_data["reading_list"].append(book)
                        file.seek(0)
                        json.dump(file_data, file, indent = 4)

                        print(f"Book {book_number} saved to Reading List\n")
        else:
            print('Please enter a valid number between 1 and 5')

        option = input("Type Number to bookmark to Reading List or 'back' to go back to options: ")

def access_reading_list():
    with open('sample.json', 'r') as file:
        file_data = json.load(file)
    
        print_books(file_data['reading_list'])  

def run_program():
    user_input = input("Find Books by Title or type 'E' to Exit: ")
    while user_input != 'E':
        if len(user_input.strip()) > 0:
            results = get_google_books(user_input)
            print(results)
            if results['totalItems'] != 0:
                print_books(results['items'])
                select_option(results)
            else:
                print('No results found, please try again.')
        else:
            print('Please enter valid search term')
        
        user_input = input("Find Books by Title or type 'E' to Exit: ")

run_program()