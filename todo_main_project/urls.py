
from django.contrib import admin
from django.urls import path, include
# from ..todo_api.urls import

urlpatterns = [
    path('admin/', admin.site.urls),
    path("todo/", include("todo_api.urls"))
]
