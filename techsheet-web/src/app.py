from flask import Flask, render_template, redirect
from src.config import Config


app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def main():
    return redirect('bot')

@app.route('/bot')
def bot():
    return render_template("index.html")

@app.route('/privacy')
def privacy():
    return render_template("privacy.html")

@app.route('/terms')
def terms():
    return render_template("terms.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
