import sqlite3

DB_NAME = "lawvista.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Cases table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_title TEXT NOT NULL,
            client_name TEXT,
            case_number TEXT,
            court TEXT,
            case_type TEXT,
            status TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Court hearings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hearings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            case_title TEXT NOT NULL,
            case_number TEXT,
            court TEXT,
            hearing_type TEXT,
            hearing_date TEXT,
            hearing_time TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Laws table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS laws (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Documents table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            document_type TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

     # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            phone TEXT,
            city TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Lawyers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lawyers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            full_name TEXT NOT NULL,
            specialization TEXT,
            bar_license TEXT,
            experience_years INTEGER DEFAULT 0,
            city TEXT,
            phone TEXT,
            email TEXT,
            bio TEXT,
            verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Judgments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS judgments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_title TEXT NOT NULL,
            citation TEXT,
            court TEXT,
            judge_name TEXT,
            decision_date TEXT,
            category TEXT,
            summary TEXT,
            judgment_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # AI legal assistant conversation history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            question TEXT NOT NULL,
            answer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Legal drafts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS legal_drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            document_type TEXT,
            title TEXT,
            client_name TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Notifications and reminders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            message TEXT,
            reminder_date TEXT,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Law student study history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            activity_type TEXT,
            topic TEXT,
            score INTEGER,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Uploaded document analysis history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            file_name TEXT NOT NULL,
            file_type TEXT,
            extracted_text TEXT,
            analysis TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Case law search history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS case_law_searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            search_query TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("LawVista database created successfully!")


def update_database():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "ALTER TABLE cases ADD COLUMN case_status TEXT DEFAULT 'Active'"
        )
    except sqlite3.OperationalError:
        pass
            # Add user ownership to cases
    try:
        cursor.execute(
            "ALTER TABLE cases ADD COLUMN user_id INTEGER"
        )
    except sqlite3.OperationalError:
        pass

    # Add user ownership to hearings
    try:
        cursor.execute(
            "ALTER TABLE hearings ADD COLUMN user_id INTEGER"
        )
    except sqlite3.OperationalError:
        pass

    conn.commit()
    conn.close()


update_database()