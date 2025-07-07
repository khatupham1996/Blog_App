Setup Instructions

1. git clone https://github.com/khatupham1996/Blog_App
   cd Journal_Blog
2. Create a virtual environment
   python -m venv venv
3. Activate the virtual environment
   .\venv\Scripts\Activate.ps1
4. Install dependencies
   pip install -r requirements.txt
5. Create the environment file
6. Appy migrations
   python manage.py migrate
7. Create a admin
   python manage.py createsuperuser
8. Collect static files
   python manage.py collectstatic
9. Run the development runserver

Features

1. User Authentication: Sign up, log in, and log out using a custom user model.
2. Journal Entries: Create, edit, and delelete blog posts with a title, content, and timestamp.
3. Categories: Tag post with zero or more categories, browse post by category.
4. Comments: Allow visitors or registered users to leave comments on posts.
5. Dynamic Interface: Use HTMX to filter, search, and paginate posts without full-page reloads.
6. Responsive Design: Styled with Tailwind CSS via Crispy Tailwind for a mobile-first, responsive layout.
