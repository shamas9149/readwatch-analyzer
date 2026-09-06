import requests

base_url="https://openlibrary.org/search.json"

def get_book_data(name):
    params = {"q": name}
    response = requests.get("https://openlibrary.org/search.json", params=params)

    if response.status_code==200:
        book_data=response.json()
        first_book=book_data["docs"][0]
        return first_book
    else:
        print( f" Failed to retrive {response.status_code}")



book_info=get_book_data("The yellow wallpaper")
if book_info:
    print(f"Name: {book_info["title"][0]}")
    print(f"Name: {book_info["author_name"][0]}")
    print(f"Name: {book_info["first_publish_year"]}")
    print(f"Name: {book_info["cover_i"]}")
    print(f"Name: {book_info["author_name"]}")
else:
    print("error")