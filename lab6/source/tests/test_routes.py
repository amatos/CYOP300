from datetime import date
from unittest.mock import ANY, patch

import pytest

import app


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


@patch("app.render_template")
@patch("app.load_post")
def test_post_route_renders_valid_post(mock_load_post, mock_render_template, client):
    mock_load_post.return_value = {
        "slug": "my-post",
        "content": "<p>content</p>",
        "date": date(2025, 1, 1),
        "summary": "",
        "tags": [],
        "title": "My Post",
    }
    mock_render_template.return_value = "POST PAGE"

    response = client.get("/post/my-post")

    assert response.status_code == 200
    assert response.data.decode() == "POST PAGE"
    mock_load_post.assert_called_once_with("my-post")
    assert mock_render_template.call_args.args[0] == "post.html"
    assert "post" in mock_render_template.call_args.kwargs


def test_post_route_rejects_invalid_slug(client):
    response = client.get("/post/bad!slug")
    assert response.status_code == 400


@patch("app.load_post")
def test_post_route_returns_404_when_post_missing(mock_load_post, client):
    mock_load_post.return_value = None

    response = client.get("/post/missing-post")

    assert response.status_code == 404


@patch("app.render_template")
def test_about_route_renders_template(mock_render_template, client):
    mock_render_template.return_value = "ABOUT PAGE"

    response = client.get("/about")

    assert response.status_code == 200
    assert response.data.decode() == "ABOUT PAGE"
    mock_render_template.assert_called_once()
    assert mock_render_template.call_args.args[0] == "about.html"


@patch("app.render_template")
def test_contact_route_renders_template(mock_render_template, client):
    mock_render_template.return_value = "CONTACT PAGE"

    response = client.get("/contact")

    assert response.status_code == 200
    assert response.data.decode() == "CONTACT PAGE"
    mock_render_template.assert_called_once()
    assert mock_render_template.call_args.args[0] == "contact.html"


@patch("app.render_template")
def test_photos_route_renders_template(mock_render_template, client):
    mock_render_template.return_value = "PHOTOS PAGE"

    response = client.get("/photos")

    assert response.status_code == 200
    assert response.data.decode() == "PHOTOS PAGE"
    mock_render_template.assert_called_once()
    assert mock_render_template.call_args.args[0] == "photos.html"


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
    mock_render_template.assert_called_once()
    assert mock_render_template.call_args.args[0] == "error.html"
    assert mock_render_template.call_args.kwargs["error_code"] == code
    assert mock_render_template.call_args.kwargs["error_description"] == description
    assert "current_time" in mock_render_template.call_args.kwargs
