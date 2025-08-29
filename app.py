#!/usr/bin/env python3
'''
VulnApp - OWASP Top 5 Vulnerability Demonstration
=================================================

⚠️  WARNING: This application intentionally contains security vulnerabilities
    for educational purposes only. NEVER use these patterns in production!

This Flask application demonstrates the OWASP 2021 Top 5 vulnerabilities:
A01 - Broken Access Control
A02 - Cryptographic Failures  
A03 - Injection
A04 - Insecure Design
A05 - Security Misconfiguration
'''

import os
import sqlite3
import hashlib
import subprocess
import requests
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from flask_cors import CORS
import logging

# A05: Security Misconfiguration - Debug mode enabled
app = Flask(__name__)
CORS(app)

# A02: Cryptographic Failures - Hardcoded weak secret key
app.secret_key = "hardcoded-secret-123"  # VULNERABILITY: Hardcoded secret

# A05: Security Misconfiguration - Debug mode enabled in production
app.config['DEBUG'] = True  # VULNERABILITY: Debug mode enabled

# Database configuration
DATABASE = 'vulnerable.db'

def get_db():
    '''Get database connection'''
    return sqlite3.connect(DATABASE)

def init_db():
    '''Initialize database with sample vulnerable data'''
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                profile TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # A02: VULNERABILITY - Insert users with plaintext passwords
        users_data = [
            ('admin', 'admin123', 'admin@vulnapp.com', 'admin', '<script>alert("XSS")</script>Admin User'),
            ('user1', 'password', 'user1@vulnapp.com', 'user', 'Regular user account'),
            ('test', 'test123', 'test@vulnapp.com', 'user', 'Test user for demonstrations'),
            ('guest', 'guest', 'guest@vulnapp.com', 'guest', 'Guest user account')
        ]

        for user_data in users_data:
            try:
                conn.execute(
                    'INSERT INTO users (username, password, email, role, profile) VALUES (?, ?, ?, ?, ?)',
                    user_data
                )
            except sqlite3.IntegrityError:
                pass  # User already exists

@app.route('/')
def index():
    '''Homepage'''
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Login page with SQL injection vulnerability'''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        # A03: VULNERABILITY - SQL Injection
        conn = get_db()
        cursor = conn.cursor()

        # VULNERABLE QUERY - Never do this!
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        try:
            cursor.execute(query)
            user = cursor.fetchone()

            if user:
                session['user_id'] = user[0]
                session['username'] = user[1] 
                session['role'] = user[4]
                return jsonify({'success': True, 'message': 'Login successful'})
            else:
                return jsonify({'success': False, 'message': 'Invalid credentials'})

        except sqlite3.Error as e:
            # A05: VULNERABILITY - Verbose error messages
            return jsonify({'success': False, 'message': f'Database error: {str(e)}'})
        finally:
            conn.close()

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST']) 
def register():
    '''Registration page'''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        email = request.form.get('email', '')

        # A02: VULNERABILITY - Store passwords in plaintext
        conn = get_db()
        try:
            conn.execute(
                'INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)',
                (username, password, email, 'user')
            )
            conn.commit()
            return jsonify({'success': True, 'message': 'Registration successful'})
        except sqlite3.IntegrityError:
            return jsonify({'success': False, 'message': 'Username already exists'})
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    '''Dashboard - missing access control'''
    # A01: VULNERABILITY - No authentication check
    username = session.get('username', 'Guest')
    return render_template('dashboard.html', username=username)

@app.route('/admin')
def admin():
    '''Admin panel - broken access control'''
    # A01: VULNERABILITY - No access control check
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    return render_template('admin.html', users=users)

@app.route('/profile')
def profile():
    '''User profile with XSS vulnerability'''
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        # A03: VULNERABILITY - XSS in profile rendering
        return render_template('profile.html', user=user)

    return redirect(url_for('login'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    '''Update user profile'''
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    user_id = session['user_id']
    profile_text = request.form.get('profile', '')
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET profile = ? WHERE id = ?', 
                      (profile_text, user_id))
        conn.commit()
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error updating profile: {str(e)}'})
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/search', methods=['GET', 'POST'])
def search():
    '''Search with SSRF vulnerability'''
    if request.method == 'POST':
        url = request.form.get('url', '')

        # A05: VULNERABILITY - Server-Side Request Forgery
        if url:
            try:
                response = requests.get(url, timeout=5)
                return jsonify({
                    'success': True,
                    'content': response.text[:1000],
                    'status_code': response.status_code
                })
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error: {str(e)}'})

    return render_template('search.html')

@app.route('/settings')
def settings():
    '''Settings page showing crypto failures'''
    # A02: VULNERABILITY - Expose configuration
    config_info = {
        'secret_key': app.secret_key,
        'debug_mode': app.config['DEBUG'],
        'database': DATABASE,
        'version': '1.0.0'
    }

    return render_template('settings.html', config=config_info)

@app.route('/logout')
def logout():
    '''Logout'''
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize database
    init_db()

    # A05: VULNERABILITY - Debug mode with public host
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
