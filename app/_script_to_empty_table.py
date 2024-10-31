"""
Scripts
---

Script to empty translation_tasks table in database.

Used for debugging purposes.

Run this script as a normal python script from local directory.

"""

# from ..database import engine
import database as db

conn = db.engine.raw_connection()

# Create a connection and Delete all rows from transaction_tasks...
cur = conn.cursor()
cur.execute("DELETE FROM translation_tasks")

conn.commit()
