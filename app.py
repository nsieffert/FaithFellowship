from flask import Flask, render_template, redirect

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)



