from flask import Flask, render_template, request, jsonify, g, send_file
import os
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

@app.route('/export')
def export():
    con = get_db_connection()
    filepath = './temp/data.csv'
    filename = 'data.csv'
    os.makedirs('./temp/', exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        for row in con.execute("select * from data_table"):
            f.write(','.join([str(c) for c in row]) + '\n')
    
    return send_file(filepath, as_attachment=True, attachment_filename=filename)


@app.route('/', methods=['POST'])
def post_json():
    received_time = int(time.time())
    json = request.get_json()  # POSTされたJSONを取得
    
    id = request.json["id"]
    name = request.json["name"]
    device_time = request.json["device_time"]
    rssi = request.json["rssi"]
    rsrp = request.json["rsrp"]
    rsrq = request.json["rsrq"]

    # データベース接続
    con = get_db_connection()
    if con.execute("select count(*) from sqlite_master where type='table'").fetchone()[0] == 0:
        con.execute("create table data_table(id integer, name varchar(10), received_time integer, device_time integer, rssi real, rsrp real, rsrq real, path varchar(20))")

    con.execute(f"insert into data_table values({id},'{name}',{received_time},{device_time},{rssi},{rsrp},{rsrq},'{name}')")

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


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)