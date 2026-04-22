"""
Author: Alberth Matos
CYOP300
Date: 21 April 2026
Description: The main entry point for the Lab 6 program. Flask executes this
module via 'flask run' or 'python3 app.py'. The application is a simple blog
site that loads markdown-formatted posts from the 'posts' directory, extracts
frontmatter metadata to display an index of posts, and contains links to the
individual posts page, a static 'about' page, a 'contacts' page, and a
'photos' page. The application also contains a custom 404 error page, as
well as links to remote sites that are relevant for blog-use.

"""

from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List

import frontmatter
import markdown
from flask import Flask, abort, render_template
from werkzeug.exceptions import HTTPException

app = Flask(__name__)


def load_posts() -> List[Dict]:
    """
    Loads and returns a list of blog posts from markdown files in the 'posts'
    directory. Each blog post is parsed to extract its metadata and content.
    The posts are sorted by date in descending order. This is used to generate
    the blog index on the main page.

    :raises FrontmatterError: If an error occurs while parsing a markdown file
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


def load_post(slug: str) -> Dict | None:
    """
    Processes a Markdown post based on the given slug. The method loads the
    corresponding Markdown file with frontmatter metadata, converts
    its content to HTML, and returns a dictionary containing the parsed data.
    If no file is found, load_post returns None.

    :param slug: Identifier for the post to be loaded, corresponds to the
        filename without extension.
    :type slug: str
    :return: A dictionary with processed post data, including HTML content,
        metadata attributes like date, summary, tags, and title, or None if
        the file cannot be loaded.
    :rtype: Dict | None
    """
    # String representing the file, with path from the application root.
    filepath = str(Path("posts").joinpath(f"{slug}.md"))
    if filepath is None:
        return None
    # Load the post data from the file
    this_post = frontmatter.load(filepath)
    # Convert the Markdown blog post content (that is, the body) to html
    html_content = markdown.markdown(this_post.content, extensions=[])
    # Return a dictionary containing the post data
    return {
        "slug": slug,
        "content": html_content,
        "date": this_post.get("date", date.min),
        "summary": this_post.get("summary", ""),
        "tags": this_post.get("tags", []),
        "title": this_post.get("title", slug.replace("-", " ").title()),
    }


@app.route("/post/<slug>")
def post(slug: str) -> str:
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
    # Basic slug validation:
    #   allow only alphanumerics and hyphens
    #   Any other character triggers an http 400 error.
    if not all(c.isalnum() or c == "-" for c in slug):
        abort(400)
    # Load the blog post data
    post_data = load_post(slug)
    # If the post data is None, throw an http 404 error, as this indicates
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
def about() -> str:
    """
    This route generates the /about page with the current timestamp
    embedded into the rendered view. It uses the Flask render_template
    function to load the HTML template.

    :return: Rendered HTML page for the about page.
    :rtype: str
    """
    return render_template(
        "about.html", current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


@app.route("/contact")
def contact() -> str:
    """
    This route generates the /contact page with the current timestamp
    embedded into the rendered view. It uses the Flask render_template
    function to load the HTML template.

    :return: Rendered HTML page for the contact page.
    :rtype: str
    """
    return render_template(
        "contact.html", current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


@app.route("/photos")
def photos() -> str:
    """
    This route generates the /photos page with the current timestamp
    embedded into the rendered view. It uses the Flask render_template
    function to load the HTML template.

    :return: Rendered HTML content for the photos page.
    :rtype: str
    """
    return render_template(
        "photos.html", current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


@app.errorhandler(404)
def not_found(e: HTTPException) -> tuple[str, Any]:
    """
    Handles 404 errors by rendering a user-friendly error page.

    This function is triggered whenever a 404 HTTP error occurs
    in the application. It returns a pre-defined 404 error
    HTML template with additional useful information to the user,
    including the current timestamp, the error code, and a brief
    description of the error.

    :param e: The error object representing the 404 HTTP error.
    :type e: flask.views.HTTPException
    :return: Rendered HTML template for the 404 error page.
    :rtype: str
    """
    return (
        render_template(
            "404.html",
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            error_code=e.code,
            error_description=e.description,
        ),
        e.code,
    )


@app.errorhandler(400)
@app.errorhandler(500)
@app.errorhandler(503)
def generic_error(e: HTTPException) -> tuple[str, Any]:
    """
    Handles 400, 500, and 503 errors by rendering a user-friendly error page.

    :param e: The error object representing the HTTP error.
    :type e: flask.views.HTTPException
    :return: Rendered HTML template for the error page.
    :rtype: str
    """
    return (
        render_template(
            "error.html",
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            error_code=e.code,
            error_description=e.description,
        ),
        e.code,
    )


if __name__ == "__main__":
    app.run()
