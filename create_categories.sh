#!/bin/bash
set -e

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create initial categories
python manage.py shell <<EOF
from tasks.models import Category
categories = ['work', 'personal', 'groceries']
for category_name in categories:
    Category.objects.get_or_create(name=category_name)
EOF

echo "This api was developed by obamwonyi destiny: https://github.com/obamwonyi"
echo "Django development server is running. Access the API at: http://localhost:8000/"
echo "Django API documentation with swagger is at: http://localhost:8000/swagger/"
# Start the Django development server
exec python manage.py runserver 0.0.0.0:8000