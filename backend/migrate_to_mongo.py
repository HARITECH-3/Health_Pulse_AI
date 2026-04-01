import sqlite3
import os
from pymongo import MongoClient
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    MONGODB_URI = os.getenv("MONGODB_URI")
    if not MONGODB_URI:
        print("MONGODB_URI not found in .env!")
        return
        
    print(f"Connecting to MongoDB Atlas...")
    client = MongoClient(MONGODB_URI)
    db = client.pulse_health_db
    
    sqlite_db_path = 'ncd_chatbot.db'
    if not os.path.exists(sqlite_db_path):
        print(f"SQLite DB {sqlite_db_path} not found.")
        return
        
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_conn.row_factory = sqlite3.Row
    cursor = sqlite_conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM users")
        sqlite_users = cursor.fetchall()
        
        migrated = 0
        skipped = 0
        for row in sqlite_users:
            user_doc = dict(row)
            # Find duplicate by email or username
            email = user_doc.get("email")
            username = user_doc.get("username")
            
            # Skip if both are empty/none (invalid row)
            if not email and not username:
                skipped += 1
                continue
                
            query = []
            if email: query.append({"email": email})
            if username: query.append({"username": username})
            
            existing = db.users.find_one({"$or": query})
            if not existing:
                # Remove sqlite id to let mongo auto-generate _id
                if 'id' in user_doc:
                    user_doc['legacy_id'] = user_doc.pop('id')
                db.users.insert_one(user_doc)
                migrated += 1
            else:
                skipped += 1
                
        print(f"Successfully migrated {migrated} users to MongoDB Atlas! (Skipped {skipped} duplicates or invalid records)")
    except Exception as e:
        print(f"Error migrating users: {e}")
        
if __name__ == '__main__':
    main()
