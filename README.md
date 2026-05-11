# Book Vault - Library Management System

Book Vault is a cinematic Flask-based Library Management System developed using Python, Flask, SQLite, HTML, CSS, and JavaScript.
The system allows users to browse, search, borrow, and return books while administrators and librarians manage the library system.

# Features

- User registration and login
- Role-based system
  - Admin
  - Librarian
  - Member
- Admin approval system
- Add, edit, and delete books
- Search books by:
  - title
  - author
  - genre
  - language
  - year
- Borrow and return books
- Fine calculation system
- Warning/reminder system
- Borrow history
- Dashboard statistics
- Animated cinematic UI
- Sound effects and magical library theme


# Technologies Used

- Python
- Flask
- SQLite
- SQLAlchemy
- HTML
- CSS
- JavaScript


# Project Structure

Book-Vault/
│
├── app.py
├── routes.py
├── models.py
├── config.py
│
├── static/
│   ├── style.css
│   ├── magic-library.mp3
│   └── page-flip.mp3
│
├── templates/
│   ├── base.html
│   ├── books.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── add_book.html
│   ├── edit_book.html
│   ├── users.html
│   ├── warnings.html
│   └── history.html
│
└── instance/
    └── library.db


# How to Run the Project

## 1. Clone the Repository

```bash
git clone https://github.com/sapidamuska/Book-Vault.git
```

## 2. Open Project Folder

```bash
cd Book-Vault
```

## 3. Install Flask

```bash
pip install flask flask_sqlalchemy
```

## 4. Run the Application

```bash
python app.py
```

## 5. Open Browser

```text
http://127.0.0.1:5000
```
Once you are logged in, you can use the following admin credentials:

Username: admin
Password: admin123

From there, you will have access to all system features. You can also test other user roles by registering a new username and password, then approving the account through the admin panel. While approving the user, you can select the specific role you want to test.

Below is a detailed preview of what each role can do.

# User Roles

## Admin

* Full system control
* Manage users
* Manage books
* Approve users

## Librarian

* Manage books
* View users
* Send warnings

## Member

* Borrow books
* Search books
* View history


# Database Tables

* User
* Book
* Borrow
* Warning
  

# Database Schema

## User Table

Stores user accounts and permissions.

| Column   | Type    | Description                 |
| -------- | ------- | --------------------------- |
| id       | Integer | Primary key                 |
| username | String  | Unique username             |
| password | String  | User password               |
| email    | String  | User email                  |
| role     | String  | Admin, librarian, or member |
| approved | Boolean | Account approval status     |


## Book Table

Stores all book information.

| Column      | Type    | Description         |
| ----------- | ------- | ------------------- |
| id          | Integer | Primary key         |
| title       | String  | Book title          |
| author      | String  | Book author         |
| year        | Integer | Publication year    |
| language    | String  | Book language       |
| genre       | String  | Book genre          |
| description | Text    | Book description    |
| available   | Boolean | Availability status |


## Borrow Table

Stores borrowing history.

| Column      | Type     | Description  |
| ----------- | -------- | ------------ |
| id          | Integer  | Primary key  |
| user_id     | Integer  | Linked user  |
| book_id     | Integer  | Linked book  |
| borrow_date | DateTime | Borrow date  |
| due_date    | DateTime | Due date     |
| return_date | DateTime | Return date  |
| fine        | Float    | Overdue fine |


## Warning Table

Stores reminders and overdue notices.

| Column     | Type     | Description         |
| ---------- | -------- | ------------------- |
| id         | Integer  | Primary key         |
| user_id    | Integer  | Related user        |
| book_id    | Integer  | Related book        |
| message    | String   | Warning message     |
| type       | String   | Reminder or overdue |
| created_at | DateTime | Date created        |


# API Endpoints / Routes

| Route          | Method    | Description       |
| -------------- | --------- | ----------------- |
| `/`            | GET       | Home page         |
| `/register`    | GET, POST | Register new user |
| `/login`       | GET, POST | Login user        |
| `/logout`      | GET       | Logout user       |
| `/dashboard`   | GET       | Dashboard         |
| `/books`       | GET       | View books        |
| `/add`         | GET, POST | Add book          |
| `/edit/<id>`   | GET, POST | Edit book         |
| `/delete/<id>` | GET       | Delete book       |
| `/search`      | GET       | Search books      |
| `/borrow/<id>` | GET       | Borrow book       |
| `/return/<id>` | GET       | Return book       |
| `/history`     | GET       | Borrow history    |
| `/warnings`    | GET       | Warning system    |
| `/users`       | GET       | Manage users      |

Developed By Sapida Muska Masood (Backend + Frontend + Testing), Hafsa Langari (Backend + Frontend + Testing), Hafizullah Khplwak (Frontend, Documentation, Testing), Mufeedullah Mamozai (Database + ERD + Testing). 
