from flask import Flask,request
app = Flask(__name__)

t = []

@app.route('/')
def index():
    return 'HELLO'

@app.route('/get-sensor')
def getTemp():
    if request.method == 'GET':
        temp = request.args.get('temperature')
        t.append(temp)
        return temp
    else:
        return 'WRONG'

@app.route('/get')
def home():
    return '<h1>{}</h1>'.format(str(t))

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')