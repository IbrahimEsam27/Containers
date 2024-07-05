from flask import Flask

app = Flask(__name__)


# the minimal Flask application
@app.route('/')
def helloworld():
    return 'Flask Hello World! ,,, Again'
@app.route('/Hema_ELgamed')
def test():
    return 'A7la Mesa 3lek ya Bro'
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=5000)
