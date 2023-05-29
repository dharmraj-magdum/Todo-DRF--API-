from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from ..serializers.todo_serializer import TodoSerializer
from ..renderer import TodoRenderer
from ..models import Todo

# //-------------------------------------------------
# create todos for logged in user
# POST "/todo/create-todo/"


class createTodoView(APIView):
    renderer_classes = [TodoRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        text = request.data.get("text")
        # print("user", user, "id", user.id)
        todo = {
            "text": text,
            "author": user.id,
        }
        print("-----------------------------todo", todo)
        serialized_data = TodoSerializer(data=todo)
        if (serialized_data.is_valid()):
            serialized_data.save()
            content = {"message": "todo added Successfully",
                       "todo": serialized_data.data}
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


# //-------------------------------------------------
# fetch todos of user
# GET "/todo/getAll/"


class getAllTodosView(APIView):
    renderer_classes = [TodoRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        todos = Todo.objects.filter(author=user.id)
        todos = TodoSerializer(todos, many=True)
        content = {"message": "all todos of "+user.name,
                   "todos": todos.data}
        return Response(content, status=status.HTTP_200_OK)


# //-------------------------------------------------
# update a todo
# POST "/todo/update-todo/todoId/"


class updateTodoView(APIView):
    renderer_classes = [TodoRenderer]
    permission_classes = [IsAuthenticated]

    def patch(self, request, todoId, format=None):
        user = request.user
        text = request.data.get("text")
        todo = None
        try:
            todo = Todo.objects.get(id=todoId, author=user.id)
        except:
            content = {
                "errors": {
                    "non_field_errors": "you are not authorized to do this changes"
                }
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        newData = {
            "text": text
        }
        serialized_data = TodoSerializer(todo, data=newData, partial=True)
        if (serialized_data.is_valid()):
            serialized_data.save()
            content = {"message": "todo updated Successfully",
                       "todo": serialized_data.data}
            return Response(content, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


# //-------------------------------------------------
# delete a todo
# POST "/todo/delete-todo/todoId/"


class deleteTodoView(APIView):
    renderer_classes = [TodoRenderer]
    permission_classes = [IsAuthenticated]

    def delete(self, request, todoId, format=None):
        user = request.user
        todo = None
        try:
            Todo.objects.get(id=todoId, author=user.id).delete()
            content = {"message": "todo deleted Successfully"}
            return Response(content, status=status.HTTP_200_OK)
        except:
            content = {
                "errors": {
                    "non_field_errors": "you are not authorized to do this changes"
                }
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
