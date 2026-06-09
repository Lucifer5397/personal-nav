import mysql.connector
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.')

@app.after_request
def add_cors(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return resp

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'pj1',
    'charset': 'utf8mb4'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)


# ==================== 书签 CRUD ====================

@app.route('/api/bookmarks', methods=['GET'])
def list_bookmarks():
    category = request.args.get('category', '')
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    if category and category != 'all':
        cursor.execute(
            'SELECT * FROM bookmarks WHERE category = %s ORDER BY sort_order, id DESC',
            (category,)
        )
    else:
        cursor.execute('SELECT * FROM bookmarks ORDER BY sort_order, id DESC')
    rows = cursor.fetchall()
    # 转换 datetime 为字符串
    for r in rows:
        for k, v in r.items():
            if hasattr(v, 'isoformat'):
                r[k] = v.isoformat()
    conn.close()
    return jsonify(rows)


@app.route('/api/bookmarks/<int:bid>', methods=['GET'])
def get_bookmark(bid):
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM bookmarks WHERE id = %s', (bid,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Not found'}), 404
    for k, v in row.items():
        if hasattr(v, 'isoformat'):
            row[k] = v.isoformat()
    return jsonify(row)


@app.route('/api/bookmarks', methods=['POST'])
def create_bookmark():
    data = request.get_json(force=True)
    title = data.get('title', '').strip()
    url = data.get('url', '').strip()
    if not title or not url:
        return jsonify({'error': 'title and url required'}), 400
    if not url.startswith('http'):
        url = 'https://' + url

    icon = data.get('icon', '🌐').strip()
    description = data.get('description', '').strip()
    category = data.get('category', 'tools').strip()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO bookmarks (title, url, description, icon, category) VALUES (%s,%s,%s,%s,%s)',
        (title, url, description, icon, category)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': new_id, 'message': 'created'}), 201


@app.route('/api/bookmarks/<int:bid>', methods=['PUT'])
def update_bookmark(bid):
    data = request.get_json(force=True)
    conn = get_db()
    cursor = conn.cursor()
    fields = []
    values = []
    for f in ['title', 'url', 'description', 'icon', 'category']:
        if f in data:
            fields.append(f'{f} = %s')
            val = data[f].strip()
            if f == 'url' and val and not val.startswith('http'):
                val = 'https://' + val
            values.append(val)
    if not fields:
        return jsonify({'error': 'no fields to update'}), 400
    values.append(bid)
    cursor.execute(f'UPDATE bookmarks SET {", ".join(fields)} WHERE id = %s', values)
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected == 0:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'message': 'updated'})


@app.route('/api/bookmarks/<int:bid>', methods=['DELETE'])
def delete_bookmark(bid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM bookmarks WHERE id = %s', (bid,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected == 0:
        return jsonify({'error': 'Not found'}), 404
    return jsonify({'message': 'deleted'})


# ==================== 分类 CRUD ====================

@app.route('/api/categories', methods=['GET'])
def list_categories():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM categories ORDER BY id')
    rows = cursor.fetchall()
    conn.close()
    for r in rows:
        for k, v in r.items():
            if hasattr(v, 'isoformat'):
                r[k] = v.isoformat()
    return jsonify(rows)


@app.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json(force=True)
    cat_key = data.get('cat_key', '').strip()
    cat_name = data.get('cat_name', '').strip()
    if not cat_key or not cat_name:
        return jsonify({'error': 'cat_key and cat_name required'}), 400
    cat_color = data.get('cat_color', '#feca57').strip()
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO categories (cat_key, cat_name, cat_color) VALUES (%s,%s,%s)',
            (cat_key, cat_name, cat_color)
        )
        conn.commit()
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'cat_key already exists'}), 409
    finally:
        conn.close()
    return jsonify({'message': 'created'}), 201


@app.route('/api/categories/<cat_key>', methods=['PUT'])
def update_category(cat_key):
    data = request.get_json(force=True)
    conn = get_db()
    cursor = conn.cursor()
    if 'cat_name' in data:
        cursor.execute('UPDATE categories SET cat_name = %s WHERE cat_key = %s', (data['cat_name'].strip(), cat_key))
    if 'cat_color' in data:
        cursor.execute('UPDATE categories SET cat_color = %s WHERE cat_key = %s', (data['cat_color'].strip(), cat_key))
    conn.commit()
    conn.close()
    return jsonify({'message': 'updated'})


@app.route('/api/categories/<cat_key>', methods=['DELETE'])
def delete_category(cat_key):
    if cat_key == 'tools':
        return jsonify({'error': 'Cannot delete default category'}), 400
    conn = get_db()
    cursor = conn.cursor()
    # 把该书签移到 tools
    cursor.execute('UPDATE bookmarks SET category = %s WHERE category = %s', ('tools', cat_key))
    cursor.execute('DELETE FROM categories WHERE cat_key = %s', (cat_key,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'deleted'})


# ==================== 静态文件 ====================

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
