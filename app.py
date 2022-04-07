from flask import Flask, render_template, request, jsonify, g
import time
import sqlite3

app = Flask(__name__)

def get_db_connection():
    if 'db_con' not in g:
        g.db_con = sqlite3.connect("data.db")
    
    return g.db_con

app.config['JSON_AS_ASCII'] = False  # JSONでの日本語文字化け対策

@app.route('/list')
def list():
    con = get_db_connection()
    cur = con.execute("select * from data_table")
    data = cur.fetchall()
    return render_template('index.html', data=data)

@app.route('/', methods=['POST'])
def post_json():
    received_time = int(time.time())
    json = request.get_json()  # POSTされたJSONを取得
    
    # テンプレートから新規登録する商品名と値段を取得
    id = request.json["id"]
    name = request.json["name"]
    device_time = request.json["device_time"]

    # データベース接続
    con = get_db_connection()
    if con.execute("select count(*) from sqlite_master where type='table'").fetchone()[0] == 0:
        con.execute("create table data_table(id integer, name varchar(10), time integer, device_time integer)")

    con.execute(f"insert into data_table values({id},'{name}',{received_time},{device_time})")

    cur = con.execute("select * from data_table")

    con.commit()
    con.close

    for c in cur:
        print(c[0], c[1])


    return jsonify(json)  # JSONをレスポンス

@app.route('/', methods=['GET'])
def get_json_from_dictionary():
    dic = {
        'key1': 'val1',
        'key2': 'val2'
    }
    return jsonify(dic)  # JSONをレスポンス