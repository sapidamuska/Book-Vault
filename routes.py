from flask import render_template, request, redirect, session
from models import db, User, Book, Borrow, Warning
from datetime import datetime
import math


# ---------------- HELPERS ----------------

def calculate_fine(due_date, return_date=None):

    today = return_date or datetime.utcnow()

    if today <= due_date:
        return 0

    days_late = (today - due_date).days
    weeks_late = math.ceil(days_late / 7)

    return weeks_late * 10


def current_user():

    if "user" in session:
        return User.query.filter_by(
            username=session["user"]
        ).first()

    return None


def is_admin():
    return session.get("role") == "admin"


def is_admin_or_librarian():
    return session.get("role") in ["admin", "librarian"]


# ---------------- ROUTES ----------------

def register_routes(app):


    # -------- HOME --------

    @app.route("/")
    def home():
        return render_template("home.html")


    # -------- AUTH --------

    @app.route("/register", methods=["GET", "POST"])
    def register():

        if request.method == "POST":

            existing_user = User.query.filter_by(
                username=request.form["username"]
            ).first()

            if existing_user:
                return "Username already exists"

            user = User(
                username=request.form["username"],
                password=request.form["password"],
                email=request.form["email"],
                role="member",
                approved=False
            )

            db.session.add(user)
            db.session.commit()

            return "Registered successfully. Wait for admin approval."

        return render_template("register.html")


    @app.route("/login", methods=["GET", "POST"])
    def login():

        if request.method == "POST":

            user = User.query.filter_by(
                username=request.form["username"]
            ).first()

            if user and user.password == request.form["password"]:

                if not user.approved:
                    return "Your account is waiting for approval."

                session["user"] = user.username
                session["role"] = user.role

                return redirect("/dashboard")

            return "Invalid username or password"

        return render_template("login.html")


    @app.route("/logout")
    def logout():

        session.clear()

        return redirect("/")


    # -------- DASHBOARD --------

    @app.route("/dashboard")
    def dashboard():

        if "user" not in session:
            return redirect("/login")

        total_books = Book.query.count()

        available_books = Book.query.filter_by(
            available=True
        ).count()

        borrowed_books = Book.query.filter_by(
            available=False
        ).count()

        total_users = User.query.count()

        recent_borrows = Borrow.query.order_by(
            Borrow.borrow_date.desc()
        ).limit(5).all()

        return render_template(
            "dashboard.html",
            total_books=total_books,
            available_books=available_books,
            borrowed_books=borrowed_books,
            total_users=total_users,
            recent_borrows=recent_borrows
        )


    # -------- BOOKS --------

    @app.route("/books")
    def books():

        if "user" not in session:
            return redirect("/login")

        books = Book.query.all()

        return render_template(
            "books.html",
            books=books
        )


    @app.route("/add", methods=["GET", "POST"])
    def add_book():

        if not is_admin_or_librarian():
            return "Access denied"

        if request.method == "POST":

            book = Book(
                title=request.form["title"],
                author=request.form["author"],
                year=int(request.form["year"]),
                language=request.form["language"],
                genre=request.form["genre"],
                description=request.form["description"]
            )

            db.session.add(book)
            db.session.commit()

            return redirect("/books")

        return render_template("add_book.html")


    @app.route("/edit/<int:id>", methods=["GET", "POST"])
    def edit_book(id):

        if not is_admin_or_librarian():
            return "Access denied"

        book = Book.query.get_or_404(id)

        if request.method == "POST":

            book.title = request.form["title"]
            book.author = request.form["author"]
            book.year = int(request.form["year"])
            book.language = request.form["language"]
            book.genre = request.form["genre"]
            book.description = request.form["description"]

            db.session.commit()

            return redirect("/books")

        return render_template(
            "edit_book.html",
            book=book
        )


    @app.route("/delete/<int:id>")
    def delete_book(id):

        if not is_admin_or_librarian():
            return "Access denied"

        book = Book.query.get_or_404(id)

        db.session.delete(book)
        db.session.commit()

        return redirect("/books")


    # -------- SEARCH --------

    @app.route("/search")
    def search():

        if "user" not in session:
            return redirect("/login")

        query = request.args.get("q", "").strip()

        books = []

        if query:

            books = Book.query.filter(

                (Book.title.ilike(f"%{query}%")) |

                (Book.author.ilike(f"%{query}%")) |

                (Book.language.ilike(f"%{query}%")) |

                (Book.genre.ilike(f"%{query}%")) |

                (Book.description.ilike(f"%{query}%"))

            ).all()

            # SEARCH BY YEAR
            if query.isdigit():

                year_books = Book.query.filter_by(
                    year=int(query)
                ).all()

                for b in year_books:

                    if b not in books:
                        books.append(b)

        return render_template(
            "search.html",
            books=books,
            query=query
        )


    # -------- BORROW --------

    @app.route("/borrow/<int:id>")
    def borrow_book(id):

        if "user" not in session:
            return redirect("/login")

        user = current_user()

        book = Book.query.get_or_404(id)

        if not book.available:
            return "Book not available"

        start_month = datetime.utcnow().replace(day=1)

        count = Borrow.query.filter(
            Borrow.user_id == user.id,
            Borrow.borrow_date >= start_month
        ).count()

        if count >= 10:
            return "Borrow limit reached (10 books per month)"

        borrow = Borrow(
            user_id=user.id,
            book_id=book.id
        )

        book.available = False

        db.session.add(borrow)
        db.session.commit()

        return redirect("/books")


    @app.route("/return/<int:id>")
    def return_book(id):

        borrow = Borrow.query.get_or_404(id)

        borrow.return_date = datetime.utcnow()

        borrow.fine = calculate_fine(
            borrow.due_date,
            borrow.return_date
        )

        borrow.book.available = True

        db.session.commit()

        return redirect("/history")


    # -------- HISTORY --------

    @app.route("/history")
    def history():

        user = current_user()

        if user.role in ["admin", "librarian"]:
            records = Borrow.query.all()

        else:
            records = Borrow.query.filter_by(
                user_id=user.id
            ).all()

        return render_template(
            "history.html",
            records=records
        )


    # -------- WARNINGS --------

    @app.route("/send-warning/<int:id>")
    def send_warning(id):

        borrow = Borrow.query.get_or_404(id)

        warning = Warning(
            user_id=borrow.user_id,
            book_id=borrow.book_id,
            message=f"Reminder: '{borrow.book.title}' is due soon.",
            type="reminder"
        )

        db.session.add(warning)
        db.session.commit()

        return redirect("/warnings")


    @app.route("/mark-overdue/<int:id>")
    def mark_overdue(id):

        borrow = Borrow.query.get_or_404(id)

        warning = Warning(
            user_id=borrow.user_id,
            book_id=borrow.book_id,
            message=f"Overdue: '{borrow.book.title}' is overdue.",
            type="overdue"
        )

        db.session.add(warning)
        db.session.commit()

        return redirect("/warnings")


    @app.route("/warnings")
    def warnings():

        user = current_user()

        if user.role in ["admin", "librarian"]:
            warnings = Warning.query.all()

        else:
            warnings = Warning.query.filter_by(
                user_id=user.id
            ).all()

        return render_template(
            "warnings.html",
            warnings=warnings
        )


    # -------- USERS --------

    @app.route("/users")
    def users():

        if not is_admin_or_librarian():
            return "Access denied"

        users = User.query.all()

        return render_template(
            "users.html",
            users=users
        )


    @app.route("/approve/<int:id>")
    def approve_user(id):

        if not is_admin_or_librarian():
            return "Access denied"

        user = User.query.get_or_404(id)

        user.approved = True

        db.session.commit()

        return redirect("/users")


    @app.route("/delete-user/<int:id>")
    def delete_user(id):

        if not is_admin():
            return "Only admin can delete users"

        user = User.query.get_or_404(id)

        db.session.delete(user)
        db.session.commit()

        return redirect("/users")


    @app.route("/edit-user/<int:id>", methods=["GET", "POST"])
    def edit_user(id):

        if not is_admin_or_librarian():
            return "Access denied"

        user = User.query.get_or_404(id)

        if request.method == "POST":

            user.username = request.form["username"]
            user.email = request.form["email"]

            if is_admin():
                user.role = request.form["role"]

            user.approved = True if request.form.get(
                "approved"
            ) == "on" else False

            db.session.commit()

            return redirect("/users")

        return render_template(
            "edit_user.html",
            user=user
        )