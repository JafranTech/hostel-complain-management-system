from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_hostel_system' # Change this in production

DB_NAME = 'complaints.db'

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                room_no TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        print("Database initialized.")

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_complaint():
    if request.method == 'POST':
        name = request.form['name']
        room_no = request.form['room_no']
        category = request.form['category']
        description = request.form['description']

        conn = get_db_connection()
        conn.execute('INSERT INTO complaints (name, room_no, category, description) VALUES (?, ?, ?, ?)',
                     (name, room_no, category, description))
        conn.commit()
        conn.close()
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Simple hardcoded admin credentials
        if username == 'jafran' and password == 'kingjafran':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    complaints = conn.execute('SELECT * FROM complaints ORDER BY timestamp DESC').fetchall()
    conn.close()
    return render_template('admin.html', complaints=complaints)

@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    new_status = request.form['status']
    conn = get_db_connection()
    conn.execute('UPDATE complaints SET status = ? WHERE id = ?', (new_status, id))
    conn.commit()
    conn.close()
    flash('Status updated successfully', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
