from flask import render_template, jsonify
from flask import Flask, request
import sqlite3

app = Flask(__name__)
application = app
app.secret_key = 'supercalifrag' # Required for flash messages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    try:
        if request.method == 'POST':
            # Grab the data from the HTML form
            name = request.form['name']
            email = request.form['email']
            message = request.form['message']

            # Connect to SQLite database (creates file if it doesn't exist)
            conn = sqlite3.connect('messages.db')
            cur = conn.cursor()

            # Create table if it does not exist
            cur.execute('''
                CREATE TABLE IF NOT EXISTS messages
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     email TEXT NOT NULL,
                     message TEXT NOT NULL,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
                        ''')

            # Insert form data into table
            cur.execute('INSERT INTO messages (name, email, message) VALUES (?, ?, ?)', (name, email, message))

            # Save changes and close the connection
            conn.commit()
            conn.close()

            # Return a successful JSON response
            return jsonify({'status': 'success', 'message': 'Your message has been sent!'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Database error: {str(e)}'}), 500

    return render_template('contact.html')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/watch')
def watch():
    return render_template('watch.html')

@app.route('/give')
def give():
    return render_template('give.html')

@app.route('/believe')
def believe():
    return render_template('believe.html')

@app.route('/studies')
def studies():
    return render_template('studies.html')

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/homeschool')
def homeschool():
    return render_template('homeschool.html')

@app.route('/terrell')
def terrell():
    return render_template('terrell.html')

@app.route('/forney')
def forney():
    return render_template('forney.html')

@app.route('/business')
def business():
    return render_template('business.html')

@app.route('/first')
def first():
    return render_template('first.html')

@app.route('/daily-verse')
def daily_verse():
    return render_template('daily-verse.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')
@app.route("/form")
def form():
    # Serve the HTML form directly
    with open("contact.html", "r") as f:
        return f.read()



if __name__ == '__main__':
    app.run(debug=True)