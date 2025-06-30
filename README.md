# Blog Application

This is a simple blog application built with Flask and WTForms. It supports creating, editing, and managing blog entries, including image uploads and tagging functionality.

## Features
- Create, edit, and delete blog entries
- Upload images to entries (supports jpg, jpeg, png, gif)
- Tag entries with multiple tags (comma-separated)
- View entries and tags
- Database migrations with Alembic

## Project Structure
- `app.py`, `main.py`, `manage.py`: Application entry points and management scripts
- `models.py`: Database models for entries and tags
- `entries/`: Blueprint for entry-related routes, forms, and templates
  - `forms.py`: WTForms forms for entries, images, and tags
  - `blueprint.py`: Blueprint routes for entry operations
  - `templates/entries/`: Jinja2 templates for entry views
- `static/`: Static files (CSS, JS, images, fonts)
- `templates/`: Base and shared templates
- `migrations/`: Alembic migration scripts

## Forms Overview
- **ImageForm**: Handles image uploads for entries, validates file type, and populates entry objects.
- **TagField**: Custom WTForms field for handling tags as comma-separated strings, supports parsing and database integration.
- **EntryForm**: Main form for creating and editing entries, includes title, body, status, slug, and tags.

## Setup
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Set up the database:
   ```sh
   python scripts/create_db.py
   ```
3. Run migrations (if needed):
   ```sh
   flask db upgrade
   ```
4. Start the application:
   ```sh
   flask run
   ```

## License
MIT License
