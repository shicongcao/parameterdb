#!/bin/bash

# Define your project directory
PROJECT_DIR="."

# Create the main app directory and subdirectories
mkdir -p $PROJECT_DIR/app/{static/css,static/js,static/images,templates,modules/auth,modules/project,modules/parameter}
mkdir -p $PROJECT_DIR/migrations
mkdir -p $PROJECT_DIR/tests

# Create HTML templates
touch $PROJECT_DIR/app/templates/{layout.html,index.html,login.html}

# Create __init__.py and other Python files inside each module
for module in auth project parameter; do
    touch $PROJECT_DIR/app/modules/$module/{__init__.py,routes.py,models.py}
done

# Create main app __init__.py and other Python files
touch $PROJECT_DIR/app/{__init__.py,models.py,forms.py,views.py}

# Create test files
touch $PROJECT_DIR/tests/{__init__.py,test_basic.py,test_models.py}

# Create main configuration files
touch $PROJECT_DIR/{config.py,run.py,requirements.txt}

# Create .env and .gitignore files
echo "__pycache__/" >> $PROJECT_DIR/.gitignore
echo "*.py[cod]" >> $PROJECT_DIR/.gitignore
echo "instance/" >> $PROJECT_DIR/.gitignore
echo ".env" >> $PROJECT_DIR/.gitignore
echo ".venv/" >> $PROJECT_DIR/.gitignore
echo "*.db" >> $PROJECT_DIR/.gitignore
echo "*.sqlite" >> $PROJECT_DIR/.gitignore

# Create an empty .env file
touch $PROJECT_DIR/.env

# Notify user of creation
echo "Project structure for '$PROJECT_DIR' has been created."

