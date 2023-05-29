from django.contrib import admin
from django.urls import path, include

from .views.userViews import userRegistrationView,\
    userLoginView,\
    userProfileView, \
    UserChangePasswordView,\
    SendPasswordResetEmailView, UserPasswordResetView,\
    userUpdateView

from .views.todoViews import createTodoView, getAllTodosView, updateTodoView, deleteTodoView

urlpatterns = []
# ------------------------------------------------------
urlpatterns += [
    path("register/", userRegistrationView.as_view(), name="register"),
    path("login/", userLoginView.as_view(), name="login"),
    path("profile/", userProfileView.as_view(), name="profile")
]
# ------------------------------------------------------
urlpatterns += [
    path('user-update/', userUpdateView.as_view(), name='userupdate'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-password-reset-email/', SendPasswordResetEmailView.as_view(),
         name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/',
         UserPasswordResetView.as_view(), name='reset-password'),
]
# ------------------------------------------------------
urlpatterns += [
    path("getAll/", getAllTodosView.as_view(), name="getall"),
    path("create-todo/", createTodoView.as_view(), name="create-todo"),
    path("update-todo/<int:todoId>/",
         updateTodoView.as_view(), name="update-todo"),
    path("delete-todo/<int:todoId>/",
         deleteTodoView.as_view(), name="delete-todo"),
]
