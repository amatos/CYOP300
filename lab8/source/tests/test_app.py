from datetime import date
from pathlib import Path
from unittest.mock import ANY, patch

import app
import pytest


class FakeFrontMatterPost:
    def __init__(self, *, content, metadata):
        self.content = content
        self._metadata = metadata

    def __contains__(self, key):
        return key in self._metadata

    def get(self, key, default=None):
        return self._metadata.get(key, default)


def test_load_posts_filters_sorts_and_maps_fields():
    fake_files = [
        Path("posts/older-post.md"),
        Path("posts/newer-post.md"),
        Path("posts/missing-title.md"),
    ]

    def fake_load(path):
        if path.endswith("older-post.md"):
            return FakeFrontMatterPost(
                content="Older content",
                metadata={
                    "date": date(2025, 1, 1),
                    "title": "Older Title",
                    "summary": "Older summary",
                    "tags": ["python"],
                },
            )
        if path.endswith("newer-post.md"):
            return FakeFrontMatterPost(
                content="Newer content",
                metadata={
                    "date": date(2026, 1, 1),
                    "title": "Newer Title",
                    "summary": "Newer summary",
                    "tags": ["flask", "pytest"],
                },
            )
        return FakeFrontMatterPost(
            content="Ignored content",
            metadata={"date": date(2024, 1, 1)},
        )

    with (
        patch("app.Path.rglob", return_value=fake_files),
        patch("app.frontmatter.load", side_effect=fake_load),
    ):
        posts = app.load_posts()

    assert len(posts) == 2
    assert posts[0]["slug"] == "newer-post"
    assert posts[1]["slug"] == "older-post"
    assert posts[0]["content"] == "Newer content"
    assert posts[0]["title"] == "Newer Title"
    assert posts[0]["summary"] == "Newer summary"
    assert posts[0]["tags"] == ["flask", "pytest"]


def test_load_post_returns_none_when_file_is_missing():
    with patch("app.Path.is_file", return_value=False):
        assert app.load_post("missing-post") is None


def test_load_post_converts_markdown_to_html():
    fake_post = FakeFrontMatterPost(
        content="# Heading\n\nSome text",
        metadata={
            "date": date(2025, 1, 1),
            "title": "My Title",
            "summary": "My Summary",
            "tags": ["tag1"],
        },
    )

    with (
        patch("app.Path.is_file", return_value=True),
        patch("app.frontmatter.load", return_value=fake_post),
        patch("app.markdown.markdown", return_value="<h1>Heading</h1><p>Some text</p>"),
    ):
        post = app.load_post("my-post")

    assert post["slug"] == "my-post"
    assert post["content"] == "<h1>Heading</h1><p>Some text</p>"
    assert post["title"] == "My Title"
    assert post["summary"] == "My Summary"
    assert post["tags"] == ["tag1"]


@patch("app.render_template")
@patch("app.load_posts")
def test_root_route_renders_index(mock_load_posts, mock_render_template, client):
    posts = [{"slug": "hello", "title": "Hello"}]
    mock_load_posts.return_value = posts
    mock_render_template.return_value = "INDEX PAGE"

    response = client.get("/")

    assert response.status_code == 200
    assert response.data.decode() == "INDEX PAGE"
    mock_load_posts.assert_called_once()
    mock_render_template.assert_called_once_with(
        "index.html",
        posts=posts,
        current_time=ANY,
    )


def test_protected_post_route_redirects_when_not_logged_in(client):
    response = client.get("/post/my-post")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login_required")


@patch("app.render_template")
@patch("app.load_post")
def test_post_route_renders_valid_post(
    mock_load_post,
    mock_render_template,
    logged_in_client,
):
    mock_load_post.return_value = {
        "slug": "my-post",
        "content": "<p>content</p>",
        "date": date(2025, 1, 1),
        "summary": "",
        "tags": [],
        "title": "My Post",
    }
    mock_render_template.return_value = "POST PAGE"

    response = logged_in_client.get("/post/my-post")

    assert response.status_code == 200
    assert response.data.decode() == "POST PAGE"
    mock_load_post.assert_called_once_with("my-post")
    mock_render_template.assert_called_once_with(
        "post.html",
        post=mock_load_post.return_value,
        current_time=ANY,
    )


def test_post_route_rejects_invalid_slug(logged_in_client):
    response = logged_in_client.get("/post/bad!slug")

    assert response.status_code == 400


@patch("app.load_post")
def test_post_route_returns_404_when_post_missing(mock_load_post, logged_in_client):
    mock_load_post.return_value = None

    response = logged_in_client.get("/post/missing-post")

    assert response.status_code == 404


@pytest.mark.parametrize(
    "route",
    [
        "/about",
        "/contact",
        "/photos",
    ],
)
def test_protected_static_routes_redirect_when_not_logged_in(route, client):
    response = client.get(route)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login_required")


@pytest.mark.parametrize(
    "route, template_name, page_text",
    [
        ("/about", "about.html", "ABOUT PAGE"),
        ("/contact", "contact.html", "CONTACT PAGE"),
        ("/photos", "photos.html", "PHOTOS PAGE"),
    ],
)
@patch("app.render_template")
def test_protected_static_routes_render_for_logged_in_user(
    mock_render_template,
    route,
    template_name,
    page_text,
    logged_in_client,
):
    mock_render_template.return_value = page_text

    response = logged_in_client.get(route)

    assert response.status_code == 200
    assert response.data.decode() == page_text
    mock_render_template.assert_called_once_with(template_name, current_time=ANY)


@patch("app.render_template")
def test_login_get_renders_login_template(mock_render_template, client):
    mock_render_template.return_value = "LOGIN PAGE"

    response = client.get("/login")

    assert response.status_code == 200
    assert response.data.decode() == "LOGIN PAGE"
    mock_render_template.assert_called_once_with(
        "login.html",
        message="",
        current_time=ANY,
    )


def test_login_redirects_if_already_logged_in(logged_in_client):
    response = logged_in_client.get("/login")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


@patch("app.db.user_is_admin")
@patch("app.db.authenticate_user")
def test_login_post_sets_session_and_redirects_on_success(
    mock_authenticate_user,
    mock_user_is_admin,
    client,
):
    mock_authenticate_user.return_value = (True, "success")
    mock_user_is_admin.return_value = True

    response = client.post(
        "/login",
        data={"username": "admin", "password": "AdminPassword1!"},
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    with client.session_transaction() as session:
        assert session["username"] == "admin"
        assert session["is_admin"] is True


@patch("app.render_template")
@patch("app.db.authenticate_user")
def test_login_post_rerenders_login_on_failure(
    mock_authenticate_user,
    mock_render_template,
    client,
):
    mock_authenticate_user.return_value = (False, "Unable to log in.")
    mock_render_template.return_value = "LOGIN PAGE"

    response = client.post(
        "/login",
        data={"username": "user@example.com", "password": "wrong"},
    )

    assert response.status_code == 200
    assert response.data.decode() == "LOGIN PAGE"
    mock_render_template.assert_called_once_with(
        "login.html",
        message="Unable to log in.",
        current_time=ANY,
    )


@patch("app.render_template")
def test_logout_clears_session_and_renders_logout(
    mock_render_template, logged_in_client
):
    mock_render_template.return_value = "LOGOUT PAGE"

    response = logged_in_client.get("/logout")

    assert response.status_code == 200
    assert response.data.decode() == "LOGOUT PAGE"

    with logged_in_client.session_transaction() as session:
        assert "username" not in session
        assert "is_admin" not in session


@patch("app.render_template")
def test_forgot_password_renders_template(mock_render_template, client):
    mock_render_template.return_value = "FORGOT PASSWORD PAGE"

    response = client.get("/forgot_password")

    assert response.status_code == 200
    assert response.data.decode() == "FORGOT PASSWORD PAGE"
    mock_render_template.assert_called_once_with(
        "forgot_password.html",
        current_time=ANY,
    )


@patch("app.render_template")
def test_create_account_get_renders_template(mock_render_template, client):
    mock_render_template.return_value = "CREATE ACCOUNT PAGE"

    response = client.get("/create_account")

    assert response.status_code == 200
    assert response.data.decode() == "CREATE ACCOUNT PAGE"
    mock_render_template.assert_called_once_with(
        "create_account.html",
        message="",
        current_time=ANY,
    )


def test_create_account_redirects_if_already_logged_in(logged_in_client):
    response = logged_in_client.get("/create_account")

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


@pytest.mark.parametrize(
    "form_data, expected_message",
    [
        (
            {
                "name": "",
                "username": "user@example.com",
                "password": "ValidPassword1!",
                "confirm_password": "ValidPassword1!",
            },
            "Name is required.",
        ),
        (
            {
                "name": "User",
                "username": "",
                "password": "ValidPassword1!",
                "confirm_password": "ValidPassword1!",
            },
            "Username is required.",
        ),
        (
            {
                "name": "User",
                "username": "user@example.com",
                "password": "",
                "confirm_password": "",
            },
            "Password is required.",
        ),
        (
            {
                "name": "User",
                "username": "user@example.com",
                "password": "ValidPassword1!",
                "confirm_password": "DifferentPassword1!",
            },
            "Passwords do not match.",
        ),
    ],
)
@patch("app.render_template")
def test_create_account_post_validates_required_fields(
    mock_render_template,
    form_data,
    expected_message,
    client,
):
    mock_render_template.return_value = "CREATE ACCOUNT PAGE"

    response = client.post("/create_account", data=form_data)

    assert response.status_code == 200
    mock_render_template.assert_called_once_with(
        "create_account.html",
        message=expected_message,
        current_time=ANY,
    )


@patch("app.db.create_user")
def test_create_account_post_sets_session_and_redirects_on_success(
    mock_create_user,
    client,
):
    mock_create_user.return_value = (True, "created")

    response = client.post(
        "/create_account",
        data={
            "name": "New User",
            "username": "new@example.com",
            "password": "ValidPassword1!",
            "confirm_password": "ValidPassword1!",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    with client.session_transaction() as session:
        assert session["username"] == "new@example.com"


@patch("app.render_template")
def test_login_required_renders_template(mock_render_template, client):
    mock_render_template.return_value = "LOGIN REQUIRED PAGE"

    response = client.get("/login_required")

    assert response.status_code == 200
    assert response.data.decode() == "LOGIN REQUIRED PAGE"
    mock_render_template.assert_called_once_with(
        "login_required.html",
        current_time=ANY,
    )


def test_user_admin_requires_admin(client):
    response = client.get("/user_admin")

    assert response.status_code == 403


@patch("app.render_template")
@patch("app.db.get_users")
def test_user_admin_get_renders_users(
    mock_get_users, mock_render_template, admin_client
):
    users = [(1, "Admin", "admin", "admin")]
    mock_get_users.return_value = (users, True, "")
    mock_render_template.return_value = "USER ADMIN PAGE"

    response = admin_client.get("/user_admin")

    assert response.status_code == 200
    assert response.data.decode() == "USER ADMIN PAGE"
    mock_render_template.assert_called_once_with(
        "user_admin.html",
        users=users,
        message="",
        current_time=ANY,
    )


@pytest.mark.parametrize(
    "action, expected_helper",
    [
        ("create_user", "create_user"),
        ("change_password", "change_password"),
        ("delete_user", "delete_user"),
    ],
)
@patch("app.render_template")
@patch("app.db.get_users")
def test_user_admin_post_dispatches_known_actions(
    mock_get_users,
    mock_render_template,
    action,
    expected_helper,
    admin_client,
):
    mock_get_users.return_value = ([], True, "")
    mock_render_template.return_value = "USER ADMIN PAGE"

    with (
        patch("app.admin.create_user", return_value="created") as mock_create_user,
        patch(
            "app.admin.change_password", return_value="changed"
        ) as mock_change_password,
        patch("app.admin.delete_user", return_value="deleted") as mock_delete_user,
    ):
        response = admin_client.post(
            "/user_admin",
            data={
                "action": action,
                "name": "User Name",
                "username": "user@example.com",
                "password": "ValidPassword1!",
            },
        )

    assert response.status_code == 200

    helper_mocks = {
        "create_user": mock_create_user,
        "change_password": mock_change_password,
        "delete_user": mock_delete_user,
    }
    helper_mocks[expected_helper].assert_called_once()


@patch("app.render_template")
@patch("app.db.get_users")
def test_user_admin_post_unknown_action_sets_message(
    mock_get_users,
    mock_render_template,
    admin_client,
):
    mock_get_users.return_value = ([], True, "")
    mock_render_template.return_value = "USER ADMIN PAGE"

    response = admin_client.post(
        "/user_admin",
        data={
            "action": "unknown",
            "username": "user@example.com",
        },
    )

    assert response.status_code == 200
    assert mock_render_template.call_args.kwargs["message"] == (
        "Unknown user administration action."
    )


@patch("app.render_template")
def test_generic_404_handler(mock_render_template, client):
    mock_render_template.return_value = "NOT FOUND"

    response = client.get("/this-route-does-not-exist")

    assert response.status_code == 404
    assert response.data.decode() == "NOT FOUND"
    mock_render_template.assert_called_once()
    assert mock_render_template.call_args.args[0] == "404.html"


@patch("app.render_template")
@pytest.mark.parametrize(
    "code, description",
    [
        (400, "Bad Request"),
        (403, "Forbidden"),
        (500, "Internal Server Error"),
        (503, "Service Unavailable"),
    ],
)
def test_generic_error_handler(mock_render_template, code, description):
    mock_render_template.return_value = "ERROR PAGE"
    error = type("E", (), {"code": code, "description": description})()

    with app.app.test_request_context():
        response = app.generic_error(error)

    assert response[0] == "ERROR PAGE"
    assert response[1] == code
    mock_render_template.assert_called_once_with(
        "error.html",
        current_time=ANY,
        error_code=code,
        error_description=description,
    )
