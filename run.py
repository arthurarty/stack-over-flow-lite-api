from app.views import app
from flask import redirect

@app.route("/")
def main():
    return redirect("apidocs/")

if __name__ == '__main__':
    app.run()
