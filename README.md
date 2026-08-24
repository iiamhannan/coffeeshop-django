# Hanni's Coffee Shop ☕

A Django web app for a coffee shop — browse the menu, place a pickup order,
and leave feedback.

## Features

- **Home / About** — informational pages about the shop
- **Menu** — search, filter by price range, and sort the coffee list
- **Order Ahead** — pick coffees + quantities, choose a pickup time, and get
  an order confirmation with a bill
- **Feedback** — customers can rate their experience and leave a message
- **Admin panel** — manage coffees, orders, and feedback at `/admin/`

## Tech stack

- Python 3 + Django 5
- SQLite (default dev database)
- Bootstrap 5 + Font Awesome (via CDN)
- Pillow (for coffee images)

## Getting started

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd coffeeshop
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **(Optional) create an admin user**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` in your browser.

> The repo ships with a demo `db.sqlite3` that already has a few coffees and
> images in `media/`, so the menu page works out of the box. Feel free to
> delete `db.sqlite3` and re-run `migrate` if you'd rather start from an
> empty database.

## Environment variables (optional)

For local development you don't need to configure anything — sensible
defaults are used. For a production deployment, set these environment
variables (see `.env.example`):

| Variable        | Purpose                                   |
|-----------------|--------------------------------------------|
| `SECRET_KEY`    | Django's cryptographic signing key         |
| `DEBUG`         | Set to `False` in production               |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hostnames  |

## Project structure

```
coffeeshop/
├── coffeeshop/       # Project settings, urls, wsgi/asgi
├── pages/            # Main app: models, views, templates, admin
│   ├── templates/    # HTML pages
│   ├── static/       # CSS
│   └── migrations/
├── media/            # Uploaded coffee images
├── manage.py
└── requirements.txt
```

## Notes / known limitations

- `DEBUG` defaults to `True`, which is fine for local development but must
  be set to `False` (with a real `SECRET_KEY` and `ALLOWED_HOSTS`) before
  deploying anywhere public.
- There's no authentication/checkout flow yet — orders are stored directly
  when the "Order Ahead" form is submitted.
