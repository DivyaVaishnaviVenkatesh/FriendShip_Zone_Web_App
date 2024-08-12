from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('friendship_zone.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            age INTEGER NOT NULL
                        )''')
        conn.commit()

init_db()

@app.route('/')
def home():
    return render_template('Homepage.html')

@app.route('/FriendList.html')
def friend_list():
    with sqlite3.connect('friendship_zone.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
    return render_template('FriendList.html', users=users)

@app.route('/RegistrationForm.html', methods=['GET', 'POST'])
def registration_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        with sqlite3.connect('friendship_zone.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', (name, email, age))
            conn.commit()
        return redirect(url_for('registration_confirmation'))
    return render_template('RegistrationForm.html')

@app.route('/RegistrationConfirmation.html')
def registration_confirmation():
    return render_template('RegistrationConfirmation.html')

@app.route('/RegistrationConfirmationforAdmin.html')
def registration_confirmation_admin():
    return render_template('RegistrationConfirmationforAdmin.html')

if __name__ == '__main__':
    app.run(debug=True)
