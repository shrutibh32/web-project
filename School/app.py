from flask import Flask, render_template, request ,redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/admission.html')
def getAdmission():
    return render_template('admission.html')
@app.route('/about-us.html')
def getAboutus():
    return render_template('about-us.html')
@app.route('/gallery.html')
def getGallery():
    return render_template('gallery.html')
@app.route('/download.html')
def getDownload():
    return render_template('download.html')
@app.route('/login.html')
def getLogin():
    return render_template('login.html')
@app.route('/admission', methods=['POST'])
def admission():
    if request.method == 'POST':
        fullName = request.form['fullName']
        fathersName = request.form['fathersName']
        mothersName = request.form['mothersName']
        number = request.form['number']
        email = request.form['email']
        _class = request.form['class']
        Address = request.form['Address']

        # SQLite database file path
        database_path = "connect.db"

        # Connect to SQLite database
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admission (
                id INTEGER PRIMARY KEY,
                fullName TEXT,
                fathersName TEXT,
                mothersName TEXT,
                number TEXT,
                email TEXT,
                class TEXT,
                Address TEXT
            )
        ''')

        # Insert data into the database
        cursor.execute('''
            INSERT INTO admission (fullName, fathersName, mothersName, number, email, class, Address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (fullName, fathersName, mothersName, number, email, _class, Address))

        conn.commit()
        conn.close()

        return "Admitted successfully"
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        # Extract data from the login form
        email = request.form['email']
        password = request.form['password']

        # Connect to SQLite database
        conn = sqlite3.connect("connect.db")
        cursor = conn.cursor()

        # Query the database for the user
        cursor.execute("SELECT * FROM logincredentials WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            # Set a session variable to indicate the user is logged in
            #session['logged_in'] = True
            return redirect('/')

        return "Login unsuccessful"  # You might want to render a login failure message here
if __name__ == '__main__':
    app.run(debug=True)
