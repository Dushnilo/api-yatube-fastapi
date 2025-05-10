from fastapi import Request
from sqladmin import ModelView

from posts.models import Group, Post, Comment
from users.models import User


class UsersAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.first_name,
                   User.last_name, User.role, User.date_joined]
    column_details_exclude_list = [User.password, User.following]
    column_sortable_list = [User.id, User.username, User.email,
                            User.first_name, User.last_name]
    name = 'User'
    name_plural = 'Users'
    icon = 'fa-duotone fa-solid fa-users'

    def is_accessible(self, request: Request) -> bool:
        self.can_create = (
            True if request.session.get('role') == 'root' else False)
        self.can_edit = (
            True if request.session.get('role') == 'root' else False)
        self.can_delete = (
            True if request.session.get('role') == 'root' else False)
        return request.session.get('role') in ['root', 'admin']


class GroupsAdmin(ModelView, model=Group):
    column_list = [Group.id, Group.title, Group.slug, Group.description]
    column_sortable_list = [Group.id, Group.title, Group.slug]
    name = 'Group'
    name_plural = 'Groups'
    icon = 'fa-solid fa-layer-group'

    def is_accessible(self, request: Request) -> bool:
        self.can_create = (
            True
            if request.session.get('role') in ('root', 'admin')
            else False
        )
        self.can_edit = (
            True
            if request.session.get('role') in ('root', 'admin')
            else False
        )
        self.can_delete = (
            True
            if request.session.get('role') in ('root', 'admin')
            else False
        )
        return request.session.get('role') in ['root', 'admin', 'moderator']


class PostsAdmin(ModelView, model=Post):
    column_list = [Post.id, Post.author, Post.text]
    column_sortable_list = [Post.id, Post.author]
    name = 'Post'
    name_plural = 'Posts'
    icon = 'fa-regular fa-comment'


class CommentsAdmin(ModelView, model=Comment):
    column_list = [Comment.id, Comment.author, Comment.text]
    column_sortable_list = [Comment.id, Comment.author]
    name = 'Comment'
    name_plural = 'Comments'
    icon = 'fa-regular fa-comments'

