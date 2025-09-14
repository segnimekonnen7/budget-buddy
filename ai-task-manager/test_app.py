from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello! The app is working!</h1>'

if __name__ == '__main__':
    print("Starting simple test app...")
    app.run(debug=True, port=5002)
