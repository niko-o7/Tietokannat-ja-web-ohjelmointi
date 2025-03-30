import sqlite3
import db
def get_threads():
    sql= """SELECT t.*, users.username
            FROM threads t
            JOIN users ON t.user_id = users.id
            GROUP BY t.id
            ORDER BY t.id DESC
            """
    return db.query(sql)

def add_thread(title, genres, grade, review, user_id):
    sql = "INSERT INTO threads (title, genres, grade, review, user_id) VALUES (?,?,?,?,?)"
    db.execute(sql, [title, genres, grade, review, user_id])
    thread_id = db.last_insert_id()
    return thread_id

def get_thread(thread_id):
    sql = "SELECT id, title FROM threads WHERE id = ?"
    return db.query(sql, [thread_id])[0]

def update_thread(thread_id, review):
    sql = "UPDATE threads SET review = ? WHERE id = ?"
    db.execute(sql, [review, thread_id])

def remove_thread(thread_id):
    sql = "DELETE FROM threads WHERE id = ?"
    db.execute(sql, [thread_id])