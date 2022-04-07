from flask import Flask, request, jsonify
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # JSONでの日本語文字化け対策

@app.route('/', methods=['POST'])
def post_json():
    json = request.get_json()  # POSTされたJSONを取得
    return jsonify(json)  # JSONをレスポンス

@app.route('/', methods=['GET'])
def get_json_from_dictionary():
    dic = {
        'key1': 'val1',
        'key2': 'val2'
    }
    return jsonify(dic)  # JSONをレスポンス