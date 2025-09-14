# Django Admin Configuration for Book Model

- Registered `Book` model in `admin.py`.
- Configured admin list view to display:
  - title
  - author
  - publication_year
- Enabled search by `title` and `author`.
- Enabled filter by `publication_year`.

## Steps to Verify:
1. Run `python manage.py runserver`.
2. Login at `/admin/` using superuser credentials.
3. Navigate to **Books** to add, edit, or delete entries.
