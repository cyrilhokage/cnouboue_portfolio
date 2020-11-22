from blog.models import Post
from github import Github
import os
import base64
import time, threading


def update_posts_from_github(username):
    # Github username
    username = "cyrilhokage"
    # pygithub object
    g = Github()
    # get that user by username
    user = g.get_user(username)


    for repo in user.get_repos():
        post, created = Post.objects.update_or_create(
            title=repo.name,
            author=username,
            updated_on=repo.pushed_at,
            created_on=repo.created_at,
            github_link=repo.svn_url,
            technos=repo.language,
            summary=repo.description, defaults={"title": "name"}
        )
        post.save()