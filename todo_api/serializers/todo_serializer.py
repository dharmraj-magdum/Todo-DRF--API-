from rest_framework import serializers
from ..models.todo import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "author", 'text', 'date']


class UpdateTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", 'text', "author", "date"]

    def create(self, validated_data):
        return Todo.objects.create(**validated_data)
