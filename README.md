# Pivot Risk Company Website

A customizable Django company website for Pivot Risk. The site includes editable company pages, projects, blog posts, team content, notices, contact messages, social links, and site-wide settings through the Django admin.

## Features

- Public home, about, services, team, contact, blog, and projects pages
- Django admin dashboard for managing website content
- Editable site settings, navigation content, notices, social links, and contact details
- Blog posts with images, PDFs, pinning, and rich content fields
- Project categories, project details, images, and downloadable assets
- SQLite database for local development
- Responsive templates with shared header, footer, and static assets

## Project structure

```text
.
├── blog/                 # Blog models, admin, views, URLs, and templates
├── company_intro/        # Django project configuration and URL routing
├── home/                 # Main pages, site settings, contact messages, and admin
├── projects/             # Project models, admin, views, URLs, and templates
├── static/               # CSS, JavaScript, fonts, and images
├── templates/            # Shared and page-level templates
├── manage.py             # Django management entry point
├── requirements.txt      # Python dependencies
└── db.sqlite3            # Local development database, when created
```

## Code map

### Request flow

```text
Browser request
  ↓
company_intro/urls.py
  ├── /admin/          → Django admin
  ├── /blog/           → blog/urls.py → blog/views.py
  ├── /projects/       → projects/urls.py → projects/views.py
  └── /                → home/urls.py → home/views.py
                                      ↓
                              templates/*.html
                                      ↓
                           static/css and static/js
```

### Application responsibilities

```text
company_intro/
├── settings.py        # Installed apps, templates, static/media, database
├── urls.py            # Root URL configuration and media routing
├── asgi.py            # ASGI deployment entry point
└── wsgi.py            # WSGI deployment entry point

home/
├── models.py          # Site settings, pages, notices, team, contacts, social links
├── views.py            # Home, about, services, team, and contact page behavior
├── sections.py        # Reusable homepage/content sections
├── admin.py           # Admin customization and content editor configuration
└── migrations/        # Database schema history

blog/
├── models.py          # Blog posts and related content fields
├── views.py           # Blog listing and detail pages
├── admin.py           # Blog editing workflows
├── urls.py            # Blog route definitions
└── templates/blog/    # Blog page templates

projects/
├── models.py          # Project categories, details, images, and downloads
├── views.py           # Project listing and detail pages
├── admin.py           # Project editing workflows
├── urls.py            # Project route definitions
└── templates/projects/# Project page templates

templates/
├── base.html           # Shared page shell, navigation, and footer
├── admin/              # Customized Django admin layout
└── home/               # Public page templates

static/
├── css/                # Public and admin stylesheets
├── js/                 # Public interactions and progressive enhancement
├── images/             # Theme and site imagery
└── fonts/              # Local font assets
```

### Where to make changes

| Goal | Primary location |
| --- | --- |
| Change branding, navigation, footer, or contact details | Django admin → Site Settings |
| Add or edit a public page | `home/models.py`, `home/views.py`, `templates/home/` |
| Change blog content | Django admin → Blog Posts; `blog/` for behavior/templates |
| Change project content | Django admin → Projects; `projects/` for behavior/templates |
| Change the visual design | `static/css/` and shared templates |
| Add client-side interactions | `static/js/` |
| Change routes | `company_intro/urls.py` or the relevant app `urls.py` |
| Change database structure | App `models.py`, then create and apply migrations |
| Change deployment configuration | `company_intro/settings.py`, `launch.sh`, and deployment files |

## Requirements

- Python 3.10 or newer
- pip
- A virtual environment is recommended

## Local setup

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open the site at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and the content editor at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## Content editing

1. Sign in at `/admin/`.
2. Update **Site Settings** first so the shared header, footer, contact details, and branding are complete.
3. Add or edit pages, team members, notices, social links, projects, categories, and blog posts.
4. Upload media through the relevant admin fields.
5. Visit the public site to review the changes.

The admin is the primary customization interface; public content should not be hardcoded into templates when a matching admin-managed model exists.

## Useful commands

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
python manage.py test
```

## Media and static files

- Static assets are stored in `static/` and served under `/static/` during development.
- Uploaded media is served under `/media/` during development.
- Uploaded files are stored within the project media paths configured in `company_intro/settings.py`.
- For production, configure a persistent media location and run `collectstatic` as part of deployment.

## Configuration and deployment

Before production deployment:

- Set a secure `SECRET_KEY` through environment variables.
- Set `DEBUG = False`.
- Configure `ALLOWED_HOSTS` for the deployment domain.
- Use a production database and persistent media storage.
- Configure HTTPS, secure cookies, and a production WSGI/ASGI server.
- Run `python manage.py check --deploy` and resolve all reported warnings.

## License

This project is maintained for the Pivot Risk company website. Add the appropriate license and ownership information before public distribution.
