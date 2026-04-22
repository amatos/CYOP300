from datetime import date
from pathlib import Path
from unittest.mock import patch

import app


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
        patch("app.frontmatter.load", return_value=fake_post),
        patch("app.markdown.markdown", return_value="<h1>Heading</h1><p>Some text</p>"),
    ):
        post = app.load_post("my-post")

    assert post["slug"] == "my-post"
    assert post["content"] == "<h1>Heading</h1><p>Some text</p>"
    assert post["title"] == "My Title"
    assert post["summary"] == "My Summary"
    assert post["tags"] == ["tag1"]
