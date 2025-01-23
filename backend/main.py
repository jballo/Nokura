from flask import Flask, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/test')
def test():
    response_body = {
        "status": "success",
        "code": 200,
        "content": "Test request."
    }
    return make_response(jsonify(response_body), 200)


if __name__ == '__main__':
    app.run()