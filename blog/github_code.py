from blog.models import Post
from github import Github
import os
import base64
import time, threading
from slugify import slugify
import requests


def get_README(repo):
    find_readme = False
    for content in repo.get_contents(""):

        if content.path == "README.md":
            find_readme = True
            return requests.get(content.download_url).text

    return find_readme


def update_posts_from_github(request, username):
    # Github username
    username = "cyrilhokage"
    # pygithub object
    g = Github()
    # get that user by username
    user = g.get_user(username)

    for repo in user.get_repos(username):

        # print(repo.name)
        name_repo = repo.name.replace("_", " ").replace("-", " ").title()
        try:
            post = Post.objects.get(title=name_repo)
            post.updated_on = repo.pushed_at
            post.github_link = repo.svn_url
            post.summary = (
                repo.description if repo.description is not None else "SUMMARY TO FILL"
            )
            post.content = get_README(repo)
        except Post.DoesNotExist:
            post, created = Post.objects.update_or_create(
                title=name_repo,
                slug=slugify(repo.name),
                author=request.user,
                updated_on=repo.pushed_at,
                created_on=repo.created_at,
                github_link=repo.svn_url,
                content=get_README(repo),
                technos=repo.language
                if repo.language is not None
                else "TECHNOS TO FILL",
                summary=repo.description
                if repo.description is not None
                else "SUMMARY TO FILL",
            )
        post.save()
