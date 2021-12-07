from myapp import app
from flask import redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('users.login'))

if __name__ == "__main__":
    app.run(debug=True)