import MySQLdb
import getpass
import os

try:
    db = MySQLdb.connect('localhost','user','pass','dbname',charset='utf8')
    pass
except:
    print("Could not establish a connection to the database. Please contact the administrator")
    os.system('pause')
    quit()
cursor = db.cursor()

admins = {
    'user': 'pass', 
    'test': '123',
    'Name': 'Password',
}


class Library:

    def __init__(self):
        self.menu()

    def ViewBooks(self):
        rs = cursor.execute("SELECT bookname FROM books;")
        if rs == 0:
            print()
            print("The Current Book Database is Empty! No books available!")
            print()
        else:
            viewbooks = cursor.fetchall()
            print()
            print("Available Books:")
            for i in viewbooks:
                print(*i)
            print()
        self.menu()

    def menu(self):
        print("1. View All Available Books.")
        print("2. Borrow a Book.")
        print("3. Return a Book.")
        print("4. Administrate the Library.")
        print("5. Exit")
        choise = input("Choose a task: ")
        while choise not in ('1','2','3','4','5',):
            print("Error! {} is not acceptable.".format(choise))
            choise = input("Choose a task: ")
        if choise == '1':
            self.ViewBooks()
        elif choise == '2':
            dt = cursor.execute("SELECT bookname FROM books;")
            if dt == 0:
                print()
                print("No Books available for borrowing right now.")
                print()
                self.menu()
            print()
            bookname = str(input("Enter the Name of Book: "))
            cursor.execute("SELECT bookname FROM books WHERE bookname = '{}';".format(bookname))
            bookdt = cursor.fetchall()
            if len(bookdt) == 0:
                print()
                print("The Desired Book is not Available for Borrowing")
                print()
                self.menu()
            fullname = str(input("Enter your Full Name: "))
            phone = str(input("Enter your Phone Number: "))
            while True:
                if (phone.isdigit() == False) or (len(phone) != 10):
                    print("Error. Phone Numbers must be only Digits and must be 10.")
                    phone = str(input("Enter your Phone Number: "))
                else:
                    break
            self.Borrow(bookname, fullname, phone)
        elif choise == '5':
            db.close()
            quit()
        elif choise == '3':
            self.ReturnBook()
        else:
            self.LibAdmin()

    def Borrow(self, bookname, fullname, phone):
        cursor.execute("DELETE FROM books WHERE bookname = '{}';".format(bookname))
        cursor.execute("INSERT INTO borrowed (bookname, fullname, phone) VALUES ('{}', '{}', '{}');".format(bookname, fullname, phone))
        db.commit()
        print()
        print("You have Borrowed the book '{}'".format(bookname))
        print()
        self.menu()

    def LibAdmin(self):
        print()
        tries = 0
        usr = input("Enter username: ")
        if usr not in admins:
            print()
            print("Administrator not found")
            print()
            self.menu()
        while True:
            if tries == 3:
                print("3 failed password attempts, exiting")
                print()
                self.menu()
            pwd = getpass.getpass("Welcome {}, enter your password: ".format(usr))
            if admins[usr] == pwd:
                print()
                print("Login successful")
                print()
                self.AdminMenu()
            else:
                tries += 1
                print("pwd attempts remaining {}".format(3-tries))

    def AdminMenu(self):
        print("1. Add a Book")
        print("2. Remove a Book")
        print("3. View All Books")
        print("4. View All Borrowed Books")
        print("5. Exit Administrator and Return")
        achoise = input("Choose a task: ")
        while achoise not in ('1','2','3','4','5',):
            print("Error. {} is not acceptable".format(achoise))
            achoise = input("Choose a task: ")
        if achoise == '1':
            self.AddBook()
        elif achoise == '2':
            self.RemoveBook()
        elif achoise == '3':
            rs = cursor.execute("SELECT bookname FROM books;")
            if rs == 0:
                print()
                print("The Current Book Database is Empty! Please add some Books!")
                print()
            else:
                viewbooks = cursor.fetchall()
                print()
                print("Available Books:")
                for i in viewbooks:
                    print(*i)
                print()
            self.AdminMenu()
        elif achoise == '5':
            print()
            print("Exiting from Administrator Mode...")
            pwd = ''
            usr= ''
            print()
            self.menu()
        else:
            self.ViewBorrowed()

    def ReturnBook(self):
        print()
        bname = input("Enter the Book Name you will Return to the Library: ")
        exist = cursor.execute("SELECT bookname FROM borrowed WHERE bookname = '{}';".format(bname))
        if exist == 0:
            print()
            print("The Book '{}' is not Borrowed".format(bname))
            print()
            self.menu()
        else:
            pnum = str(input("Enter your Phone Number: "))
            fname = input("Enter your Full Name: ")
            auths = cursor.execute("SELECT * FROM borrowed;")
            auth = cursor.fetchall()
            i = 0
            while i != len(auth):
                    if auth[i][2] == pnum and auth[i][0] == bname and auth[i][1] == fname:
                        cursor.execute("INSERT INTO books (bookname) VALUES ('{}');".format(bname))
                        cursor.execute("DELETE FROM borrowed WHERE bookname = '{}' AND fullname = '{}' AND phone = '{}';".format(bname, fname, pnum))
                        db.commit()
                        print()
                        print("The Book '{}' has been Returned to the Library. Thank you {} for using our Library.".format(bname, fname))
                        print()
                        self.menu()
                    else:
                        i += 1
            else:
                print()
                print("Authentication Failed! Credentials do not match, Try Again.")
                print()
                self.menu()

    def AddBook(self):
        newbookname = str(input("Enter the Name of the New Book: "))
        cursor.execute("SELECT bookname FROM books WHERE bookname = '{}'".format(newbookname))
        ex = cursor.fetchall()
        if len(ex) == 0:
            cursor.execute("INSERT INTO books (bookname) VALUES ('{}');".format(newbookname))
            db.commit()
            print()
            print("New Book '{}' has been Added!".format(newbookname))
            print()
            self.AdminMenu()
        else:
            print()
            print("The Book '{}' alredy exists in our database".format(newbookname))
            print()
            self.AdminMenu()

    def RemoveBook(self):
        bookname2 = str(input("Enter the Name of the Book you want to Remove: "))
        cursor.execute("SELECT bookname FROM books WHERE bookname = '{}';".format(bookname2))
        ex = cursor.fetchall()
        if len(ex) == 0:
            print()
            print("Could not find '{}' in our database".format(bookname2))
            print()
        else:
            cursor.execute("DELETE FROM books WHERE bookname = '{}'".format(bookname2))
            db.commit()
            print()
            print("'{}' Has been successfully removed from our database".format(bookname2))
            print()
        self.AdminMenu()

    def ViewBorrowed(self):
        brd = cursor.execute("SELECT * FROM borrowed;")
        if brd == 0:
            print()
            print("No Borrowers at the moment. 0 Books Borrowed.")
            print()
            self.AdminMenu()
        else:
            brdb = cursor.fetchall()
            for row in brdb:
                borrowerbookname = row[0]
                borrowername = row[1]
                borrowerphone = row[2]
                print("Book Name:", (borrowerbookname) , " Borrower Name:", (borrowername) , " Borrower Phone Number:", (borrowerphone))
                print()
            self.AdminMenu()

Library()
 
