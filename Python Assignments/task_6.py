class Library:
    def __init__(self):
        self.books = []

    def add_book(self, title):
        self.books.append(title)

    def remove_book(self, title):
        if title in self.books:
            self.books.remove(title)

    def search_by_title(self, query):
        return [b for b in self.books if query.lower() in b.lower()]


lib = Library()
lib.add_book("The Great Gatsby")
lib.add_book("1984")
print(lib.search_by_title("great"))
lib.remove_book("1984")
print(lib.books)
