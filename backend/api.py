from flask import Blueprint, jsonify, request
import sqlite3
import os

api_bp = Blueprint('api', __name__)

BASE_DIR = os.path.dirname(__file__)  # backend/
DB_DIR = os.path.join(BASE_DIR, 'db')
DATABASE = os.path.join(DB_DIR, 'book_club.db')
SCHEMA_PATH = os.path.join(DB_DIR, 'schema.sql')

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    need_schema = True
    if os.path.exists(DATABASE):
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='members';")
            need_schema = cur.fetchone() is None
        except Exception:
            need_schema = True
        finally:
            try:
                conn.close()
            except Exception:
                pass

    if need_schema:
        if not os.path.exists(SCHEMA_PATH):
            raise RuntimeError(f"Schema file not found: {SCHEMA_PATH}")
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        conn = sqlite3.connect(DATABASE)
        try:
            conn.executescript(schema_sql)
        finally:
            conn.close()

def get_db_connection():
    # allow use from Flask threaded environment
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# initialize DB at import
init_db()

# --- Members ---
@api_bp.route('/api/members', methods=['GET'])
def get_members():
    conn = get_db_connection()
    try:
        members = conn.execute('SELECT * FROM members ORDER BY joined_date DESC').fetchall()
        return jsonify([dict(member) for member in members])
    finally:
        conn.close()

@api_bp.route('/api/members', methods=['POST'])
def add_member():
    new_member = request.get_json(silent=True)
    if not new_member or 'name' not in new_member or 'email' not in new_member:
        return jsonify({'error': 'name and email required'}), 400
    conn = get_db_connection()
    try:
        cur = conn.execute('INSERT INTO members (name, email) VALUES (?, ?)',
                    (new_member['name'].strip(), new_member['email'].strip()))
        conn.commit()
        member_id = cur.lastrowid
        row = conn.execute('SELECT * FROM members WHERE id = ?', (member_id,)).fetchone()
        return jsonify(dict(row)), 201
    except sqlite3.IntegrityError as e:
        return jsonify({'error': 'email must be unique'}), 400
    finally:
        conn.close()

@api_bp.route('/api/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    conn = get_db_connection()
    try:
        # remove loans referencing this member first
        conn.execute('DELETE FROM loans WHERE member_id = ?', (member_id,))
        cur = conn.execute('DELETE FROM members WHERE id = ?', (member_id,))
        conn.commit()
        if cur.rowcount and cur.rowcount > 0:
            return jsonify({'message': 'member deleted'}), 200
        else:
            return jsonify({'error': 'member not found'}), 404
    finally:
        conn.close()

# --- Books ---
@api_bp.route('/api/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    try:
        books = conn.execute('SELECT * FROM books ORDER BY id DESC').fetchall()
        return jsonify([dict(book) for book in books])
    finally:
        conn.close()

@api_bp.route('/api/books', methods=['POST'])
def add_book():
    new_book = request.get_json(silent=True)
    if not new_book or 'title' not in new_book or 'author' not in new_book:
        return jsonify({'error': 'title and author required'}), 400
    conn = get_db_connection()
    try:
        cur = conn.execute('INSERT INTO books (title, author) VALUES (?, ?)',
                     (new_book['title'].strip(), new_book['author'].strip()))
        conn.commit()
        book_id = cur.lastrowid
        row = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        return jsonify(dict(row)), 201
    finally:
        conn.close()

@api_bp.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db_connection()
    try:
        # remove loans referencing this book first
        conn.execute('DELETE FROM loans WHERE book_id = ?', (book_id,))
        cur = conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        if cur.rowcount and cur.rowcount > 0:
            return jsonify({'message': 'book deleted'}), 200
        else:
            return jsonify({'error': 'book not found'}), 404
    finally:
        conn.close()

# --- Lending ---
@api_bp.route('/api/lend', methods=['POST'])
def lend_book():
    data = request.get_json(silent=True)
    if not data or 'member_id' not in data or 'book_id' not in data:
        return jsonify({'error': 'member_id and book_id required'}), 400
    conn = get_db_connection()
    try:
        m = conn.execute('SELECT * FROM members WHERE id = ?', (data['member_id'],)).fetchone()
        b = conn.execute('SELECT * FROM books WHERE id = ?', (data['book_id'],)).fetchone()
        if not m or not b:
            return jsonify({'error': 'member or book not found'}), 404
        if b['available'] == 0:
            return jsonify({'error': 'book not available'}), 400
        cur = conn.execute('INSERT INTO loans (member_id, book_id) VALUES (?, ?)',
                     (data['member_id'], data['book_id']))
        conn.execute('UPDATE books SET available = 0 WHERE id = ?', (data['book_id'],))
        conn.commit()
        loan_id = cur.lastrowid
        row = conn.execute('SELECT * FROM loans WHERE id = ?', (loan_id,)).fetchone()
        return jsonify(dict(row)), 201
    finally:
        conn.close()

@api_bp.route('/api/loans', methods=['GET'])
def get_loans():
    conn = get_db_connection()
    try:
        loans = conn.execute('''
            SELECT l.*, m.name as member_name, b.title as book_title 
            FROM loans l
            JOIN members m ON l.member_id = m.id
            JOIN books b ON l.book_id = b.id
            WHERE l.return_date IS NULL
            ORDER BY l.loan_date DESC
        ''').fetchall()
        return jsonify([dict(loan) for loan in loans])
    finally:
        conn.close()

@api_bp.route('/api/loans/<int:loan_id>/return', methods=['POST'])
def return_book(loan_id):
    conn = get_db_connection()
    try:
        # Get book_id before updating
        loan = conn.execute('SELECT book_id FROM loans WHERE id = ?', (loan_id,)).fetchone()
        if not loan:
            return jsonify({'error': 'loan not found'}), 404
            
        # Update return date and book availability
        conn.execute('UPDATE loans SET return_date = CURRENT_TIMESTAMP WHERE id = ?', (loan_id,))
        conn.execute('UPDATE books SET available = 1 WHERE id = ?', (loan['book_id'],))
        conn.commit()
        return jsonify({'message': 'book returned successfully'}), 200
    except Exception as e:
        pass
    finally:
        conn.close()    
        conn.close()