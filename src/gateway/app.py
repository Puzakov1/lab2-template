from flask import Flask, request, jsonify, make_response

app = Flask(__name__)


@app.route('/manage/health', methods=['GET'])
def health_check():
    return 200


if __name__ == '__main__':
    app.run(port=8050)