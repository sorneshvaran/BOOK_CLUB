class Book:
    def __init__(self, id, title, author):
        self.id = id
        self.title = title
        self.author = author

    def create_book(self, title, author):
        # Logic to create a new book in the database
        pass

    def update_book(self, id, title=None, author=None):
        # Logic to update an existing book in the database
        pass

    def delete_book(self, id):
        # Logic to delete a book from the database
        pass

    @staticmethod
    def get_book_by_id(id):
        # Logic to retrieve a book by its ID from the database
        pass

    @staticmethod
    def get_all_books():
        # Logic to retrieve all books from the database
        pass