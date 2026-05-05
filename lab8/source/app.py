"""
Author: Alberth Matos
CYOP300
Date: 28 April 2026
Description: The main entry point for the Lab 7 program. Flask executes this
module via 'flask run' or 'python3 app.py'. This program makes use of helper
modules to handle db operations, and handle tasks on the user admin page.

"""

import os
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List

import frontmatter
import markdown
from flask import Flask, abort, redirect, render_template, request, session
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers.response import Response

import admin
import db

# Define module-wide constants.
app = Flask(__name__)
# app.secret_key is used to sign the session cookie to prevent tampering.
# In this case, we import a value from the running environment, as would be
# done in the real world, or fall back to a lorum ipsum if one is not provided.
app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do "
    "eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad "
    "minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip "
    "ex ea commodo consequat. Duis aute irure dolor in reprehenderit in "
    "voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur "
    "sint occaecat cupidatat non proident, sunt in culpa qui officia "
    "deserunt mollit anim id est laborum.",
)


def load_posts() -> List[Dict[str, Any]]:
    """
    Loads and returns a list of blog posts from Markdown files in the 'posts'
    directory. Each blog post is parsed to extract its metadata and content.
    The posts are sorted by date in descending order. This is used to generate
    the blog index on the main page.

    :raises FrontmatterError: If an error occurs while parsing a Markdown file
        with frontmatter.

    :return: A list of dictionaries, where each dictionary represents a blog
        post. Each dictionary includes
        the following keys:

        - slug (str): The filename's stem, used as a unique identifier.
        - content (str): The main text content of the blog post.
        - date (datetime.date): The date associated with the blog post. This
            is a REQUIRED field.
        - summary (str): A short description or summary of the blog post.
            - tags (List[str]): The tags associated with the blog post.
        - title (str): The title of the blog post. This is a REQUIRED field.
    :rtype: List[Dict]
    """

    # Initialize empty list to contain blog post dictionary.
    my_posts = []
    # Build a list of all files with .md extensions in the posts directory.
    post_files = list(Path("posts").rglob("*.md"))
    for file in post_files:
        # For each file:
        #    set the slug to the file's stem (the filename without the extension)
        #    Load the blog entry content from the file
        #    Add the blog entry's date
        #    Add the blog entry's summary, if provided
        #    Add the blog entry's tags, if provided
        #    Add the blog entry's title
        slug = file.stem
        this_post = frontmatter.load(str(file))
        if "date" in this_post and "title" in this_post:
            my_posts.append(
                {
                    "slug": slug,
                    "content": this_post.content,
                    "date": this_post.get("date", date.min),
                    "summary": this_post.get("summary", ""),
                    "tags": this_post.get("tags", []),
                    "title": this_post.get("title", slug.replace("-", " ").title()),
                }
            )
    # Sort all posts by date, in descending order
    my_posts.sort(key=lambda p: p["date"], reverse=True)
    return my_posts


def load_post(slug: str) -> Dict[str, Any] | None:
    """
    Processes a Markdown post based on the given slug. The method loads the
    corresponding Markdown file with frontmatter metadata, converts
    its content to HTML, and returns a dictionary containing the parsed data.
    If no file is found, load_post returns None.
    """
    filepath = Path("posts").joinpath(f"{slug}.md")

    if not filepath.is_file():
        return None

    this_post = frontmatter.load(str(filepath))
    html_content = markdown.markdown(this_post.content, extensions=[])

    return {
        "slug": slug,
        "content": html_content,
        "date": this_post.get("date", date.min),
        "summary": this_post.get("summary", ""),
        "tags": this_post.get("tags", []),
        "title": this_post.get("title", slug.replace("-", " ").title()),
    }


@app.route("/post/<slug>")
def post(slug: str) -> str | Response:
    """
    This function validates the slug provided in the URL to ensure it only contains
    alphanumeric characters and hyphens. If the validation fails, a 400 HTTP status
    code is returned. If the post corresponding to the slug is not found, a 404 HTTP
    status is returned. Otherwise, the post data is rendered using the 'post'
    template, along with the current timestamp.

    :param slug: Unique identifier for the blog post, provided in the URL.
    :type slug: str
    :return: Rendered HTML template of the blog post.
    :rtype: str
    """

    if "username" not in session:
        return redirect("/login_required")

    # Basic slug validation:
    #   allow only alphanumerics and hyphens
    #   Any other character triggers an http 400 error.
    if not all(c.isalnum() or c == "-" for c in slug):
        abort(400)
    # Load the blog post data
    post_data = load_post(slug)
    # If post data is None, throw an http 404 error, as this indicates
    # that the post does not exist.
    if post_data is None:
        abort(404)
    # Otherwise, render the post using the 'post' template, along with the
    # current timestamp.
    return render_template(
        "post.html",
        post=post_data,
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/")
def root() -> str:
    """
    This function processes and loads the posts by invoking the
    load_posts function and renders them onto the "index.html"
    template. It also adds the current timestamp to the rendered template.

    :return: Rendered HTML page for the main/root page.
    :rtype: str
    """
    # list of dictionaries containing blog entries.
    posts = load_posts()
    # Render the index.html template, passing the list of posts and the current
    # timestamp.
    return render_template(
        "index.html",
        posts=posts,
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/about")
def about() -> str | Response:
    """
    This route generates the /about page with the current timestamp
    embedded into the rendered view. It uses the Flask render_template
    function to load the HTML template.

    :return: Rendered HTML page for the about page.
    :rtype: str
    """
    if "username" not in session:
        return redirect("/login_required")
    return render_template(
        "about.html", current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


@app.route("/contact")
def contact() -> str | Response:
    """
    This route generates the /contact page with the current timestamp
    embedded into the rendered view. It uses the Flask render_template
    function to load the HTML template.

    :return: Rendered HTML page for the contact page.
    :rtype: str
    """
    if "username" not in session:
        return redirect("/login_required")
    return render_template(
        "contact.html", current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


@app.route("/photos")
def photos() -> str | Response:
    """
    This route generates the /photos page with the current timestamp
    embedded into the rendered view. It uses the Flask render_template
    function to load the HTML template.

    :return: Rendered HTML content for the photos page.
    :rtype: str
    """
    if "username" not in session:
        return redirect("/login_required")
    return render_template(
        "photos.html", current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


@app.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    """
    Handles user login functionality. This function manages both GET and POST requests.
    For GET requests, it renders the login page. For POST requests, it processes the
    incoming username and password, authenticates the user, and either redirects them to
    the home page (if login is successful) or re-renders the login page with an error
    message.

    :param methods: The allowed HTTP methods for this route, which are GET and POST.
    :return: For authenticated users, a redirect response to the home page. For
        unauthenticated users, the login form is re-rendered with an error message.
    :rtype: str | Response
    """
    if "username" in session:
        return redirect("/")

    message = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        # call the authenticate_user function from the db module to check if
        # the user exists, and has provided the correct password.
        authenticated, message = db.authenticate_user(username, password)
        if authenticated:
            # If the user is authenticated, set the session variable
            # 'username', and check if the user is an admin.
            session["username"] = username
            session["is_admin"] = db.user_is_admin(username)
            return redirect("/")

    return render_template(
        "login.html",
        message=message,
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/logout")
def logout() -> str:
    """
    Logs out the current user by clearing the session and displays a logout
    confirmation page.

    :return: Rendered HTML page confirming the user has logged out.
    :rtype: str
    """
    session.clear()

    return render_template(
        "logout.html",
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/forgot_password")
def forgot_password() -> str:
    """
    Display a page where the user can request a password reset.

    Or rather, a page that would do that, if the functionality were implemented.

    :return: Rendered HTML page confirming the user has logged out.
    :rtype: str
    """

    return render_template(
        "forgot_password.html",
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/create_account", methods=["GET", "POST"])
def create_account() -> str | Response:
    """
    This route generates the create account page with the current timestamp
    embedded into the rendered view.

    :return: Rendered HTML page for the create account page.
    :rtype: str
    """
    # if the username is set in the session, then the user does not need to
    # create an account. Redirect them to the home page instead.
    # Note: the create/login pages should not display to logged in users.
    if "username" in session:
        return redirect("/")

    message = ""

    if request.method == "POST":
        # Get the form data and strip any whitespace from the username and password.
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        # Perform validation checks on the form data.
        if not name:
            message = "Name is required."
        elif not username:
            message = "Username is required."
        elif not password:
            message = "Password is required."
        elif password != confirm_password:
            message = "Passwords do not match."
        else:
            # If all validation checks pass, create the user account.
            user_created, message = db.create_user(name, username, password)

            if user_created:
                # If the user is created, set the session variable
                # 'username', and redirect them to the home page.
                session["username"] = username
                return redirect("/")

    return render_template(
        "create_account.html",
        message=message,
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/login_required")
def login_required() -> str:
    """
    This route generates a page informing users that they must log in before
    accessing protected content.

    :return: Rendered HTML page for the login required notice.
    :rtype: str
    """
    return render_template(
        "login_required.html",
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.route("/user_admin", methods=["GET", "POST"])
def user_admin() -> Response | str:
    """
    This route generates the user administration page. Administrators can view,
    create, and delete users, and change user passwords.
    :return: Rendered HTML page for user administration.
    :rtype: str
    """
    if not session.get("is_admin", False):
        abort(403)

    message = ""
    users = []

    if request.method == "POST":
        # Get the form data and strip any whitespace from the username and password.
        action = request.form.get("action", "")
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        # Perform various actions depending on the form data.
        if not username:
            message = "Username is required."
        if action == "create_user":
            message = admin.create_user(name=name, username=username, password=password)
        elif action == "change_password":
            message = admin.change_password(username, password)
        elif action == "delete_user":
            message = admin.delete_user(username, session["username"])
        else:
            message = "Unknown user administration action."

    # For a Get method, get list of users from the database and display it
    # on the page.
    users, succeeded, get_user_message = db.get_users()
    if not succeeded:
        message = get_user_message

    return render_template(
        "user_admin.html",
        users=users,
        message=message,
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


@app.errorhandler(404)
def not_found(e: HTTPException) -> tuple[str, int]:
    """
    Handles 404 errors by rendering a user-friendly error page.

    This function is triggered whenever a 404 HTTP error occurs
    in the application. It returns a pre-defined 404 error
    HTML template with additional useful information to the user,
    including the current timestamp, the error code, and a brief
    description of the error.

    :param e: The error object representing the 404 HTTP error.
    :type e: werkzeug.exceptions.HTTPException
    :return: Rendered HTML template for the 404 error page.
    :rtype: str
    """
    status_code = getattr(e, "code", 404)
    description = getattr(e, "description", "An unexpected error occurred.")
    return (
        render_template(
            "404.html",
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            error_code=status_code,
            error_description=description,
        ),
        status_code,
    )


@app.errorhandler(400)
@app.errorhandler(403)
@app.errorhandler(500)
@app.errorhandler(503)
def generic_error(e: HTTPException) -> tuple[str, int]:
    """
    Handles 400, 403, 500, and 503 errors by rendering a user-friendly error page.

    :param e: The error object representing the HTTP error.
    :type e: flask.views.HTTPException
    :return: Rendered HTML template for the error page.
    :rtype: str
    """
    status_code = getattr(e, "code", 500)
    description = getattr(e, "description", "An unexpected error occurred.")
    return (
        render_template(
            "error.html",
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            error_code=status_code,
            error_description=description,
        ),
        status_code,
    )


if __name__ == "__main__":
    app.run()
