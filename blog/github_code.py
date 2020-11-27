from blog.models import Post
from github import Github
import os
import base64
import time, threading
from slugify import slugify

def update_posts_from_github(request, username):
    # Github username
    username = "cyrilhokage"
    # pygithub object
    g = Github()
    # get that user by username
    user = g.get_user(username)


    for repo in user.get_repos(username):

        print(repo.name)
        post, created = Post.objects.update_or_create(
            title=repo.name,
            slug = slugify(repo.name),
            author=request.user,
            updated_on=repo.pushed_at,
            created_on=repo.created_at,
            github_link=repo.svn_url,
            technos=repo.language if repo.language is not None else "TECHNOS TO FILL",
            summary=repo.description if repo.description is not None else "SUMMARY TO FILL",
        )
        post.save()