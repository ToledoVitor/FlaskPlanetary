from flask import Flask, jsonify, request

app = Flask(__name__)
# Makes server reload in real time
app.debug = True


@app.route('/')
def hello_world():
    return jsonify(message='Hello World!'), 200


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the Planetary API!'), 200


@app.route('/not_found')
def not_found():
    return jsonify(message='Resource not found'), 404


@app.route('/parameters')
def parameters():
    name = str(request.args.get('name'))
    age = int(request.args.get('age'))

    if age < 18:
        return jsonify(message=f'sorry, {name}, you are not old enough'), 403
    return jsonify(message=f'welcome {name}, you are old enough'), 200


@app.route('/url_parameters/<string:name>/<int:age>')
def url_parameters(name: str, age: int):
    if age < 18:
        return jsonify(message=f'sorry, {name}, you are not old enough'), 403
    return jsonify(message=f'welcome {name}, you are old enough'), 200


if __name__ == '__main__':
    app.run()