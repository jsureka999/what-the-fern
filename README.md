# What the Fern - Plant Shop Website

A complete plant shop website with contact form, database storage, user authentication, and admin panel.

## Features

- 🌿 **Plant Shop Website** - Beautiful, responsive design
- 📧 **Contact Form** - Collect customer inquiries
- 🗄️ **SQL Database** - Store contact submissions securely
- 🔐 **User Authentication** - Secure admin access
- 📊 **Admin Panel** - View and manage contact submissions
- 📈 **Statistics Dashboard** - Track submissions over time
- 📄 **CSV Export** - Export contact data to CSV files
- 🏷️ **Status Management** - Mark submissions as new, read, or replied

## Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

### 3. Create Admin User

Visit `http://localhost:5000/setup` to create the initial admin user:
- **Username**: admin
- **Password**: admin123

### 4. Access the Website

- **Main Website**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **Login Page**: http://localhost:5000/login

## Database

The application uses SQLite by default, which creates a `whatthefern.db` file in your project directory.

### Database Schema

**Users Table:**
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- is_admin (Boolean)

**Contacts Table:**
- id (Primary Key)
- first_name
- last_name
- email
- message
- timestamp
- status (new/read/replied)

## Admin Features

### Dashboard Statistics
- Total submissions
- Today's submissions
- New unread submissions

### Contact Management
- View all contact submissions
- Update submission status
- Export data to CSV
- Sort by date (newest first)

### Security
- Password-protected admin access
- Session management
- CSRF protection

## File Structure

```
what-the-fern-site/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── whatthefern.db        # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── index.html
│   ├── shop.html
│   ├── plants.html
│   ├── contact.html
│   ├── admin.html
│   └── login.html
├── static/               # Static files
│   ├── style.css
│   └── images/
└── README.md
```

## Production Deployment

For production deployment, consider:

1. **Change the secret key** in `app.py`
2. **Use a production database** (MySQL/PostgreSQL)
3. **Set up HTTPS** with SSL certificates
4. **Use a production WSGI server** (Gunicorn, uWSGI)
5. **Set up email notifications** for new submissions
6. **Add rate limiting** to prevent spam
7. **Implement backup strategies** for the database

## Security Notes

- Change the default admin password after first login
- Keep the secret key secure and unique
- Regularly backup the database
- Monitor for suspicious activity

## Support

For issues or questions, please contact the development team. 