from fastapi import FastAPI
from sqladmin import Admin

from admin.admin import UsersAdmin, GroupsAdmin, PostsAdmin, CommentsAdmin
from database import engine

from admin.auth import authentication_backend
from comments.router import router as router_comments
from groups.router import router as router_groups
from posts.router import router as router_posts
from users.router import router as router_users


app = FastAPI()
app.include_router(router_posts)
app.include_router(router_comments)
app.include_router(router_groups)
app.include_router(router_users)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(GroupsAdmin)
admin.add_view(PostsAdmin)
admin.add_view(CommentsAdmin)
# 
