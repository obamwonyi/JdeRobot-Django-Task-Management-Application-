from rest_framework import serializers
from tasks.models import Task, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'priority', 'completed',
            'category', 'category_id', 'due_date', 'created_at', 'updated_at', 'order'
        ]
        read_only_fields = ['created_at', 'updated_at']

    title = serializers.CharField(required=True)