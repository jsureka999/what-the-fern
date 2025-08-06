from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import io
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///whatthefern.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='new')  # new, read, replied

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/plants')
def plants():
    return render_template('plants.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    data = request.json
    contact = Contact(
        first_name=data['firstName'],
        last_name=data['lastName'],
        email=data['email'],
        message=data['message']
    )
    db.session.add(contact)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Message sent successfully!'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    
    contacts = Contact.query.order_by(Contact.timestamp.desc()).all()
    stats = {
        'total': Contact.query.count(),
        'today': Contact.query.filter(
            Contact.timestamp >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        ).count(),
        'new': Contact.query.filter_by(status='new').count()
    }
    
    return render_template('admin.html', contacts=contacts, stats=stats)

@app.route('/api/contacts')
@login_required
def get_contacts():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    contacts = Contact.query.order_by(Contact.timestamp.desc()).all()
    return jsonify([{
        'id': c.id,
        'firstName': c.first_name,
        'lastName': c.last_name,
        'email': c.email,
        'message': c.message,
        'timestamp': c.timestamp.isoformat(),
        'status': c.status
    } for c in contacts])

@app.route('/api/contacts/<int:contact_id>/status', methods=['PUT'])
@login_required
def update_contact_status(contact_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    contact = Contact.query.get_or_404(contact_id)
    data = request.json
    contact.status = data['status']
    db.session.commit()
    return jsonify({'success': True})

@app.route('/export/csv')
@login_required
def export_csv():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    contacts = Contact.query.order_by(Contact.timestamp.desc()).all()
    
    # Create CSV in memory
    si = io.StringIO()
    cw = csv.writer(si)
    
    # Write header
    cw.writerow(['ID', 'First Name', 'Last Name', 'Email', 'Message', 'Timestamp', 'Status'])
    
    # Write data
    for contact in contacts:
        cw.writerow([
            contact.id,
            contact.first_name,
            contact.last_name,
            contact.email,
            contact.message,
            contact.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            contact.status
        ])
    
    output = si.getvalue()
    si.close()
    
    return send_file(
        io.BytesIO(output.encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'contacts_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

@app.route('/setup')
def setup():
    """Initial setup - creates admin user"""
    if User.query.first():
        return "Admin user already exists!"
    
    admin_user = User(
        username='admin',
        email='admin@whatthefern.com',
        password_hash=generate_password_hash('admin123'),
        is_admin=True
    )
    db.session.add(admin_user)
    db.session.commit()
    return "Admin user created! Username: admin, Password: admin123"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000) 