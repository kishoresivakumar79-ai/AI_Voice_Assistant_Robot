import sqlite3
import os

def init_databases():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_dir, "schema.sql")
    
    with open(schema_path, "r") as f:
        sql_script = f.read()

    # Create robot.db
    robot_db = os.path.join(base_dir, "robot.db")
    conn = sqlite3.connect(robot_db)
    conn.executescript(sql_script)
    
    # Insert default configs
    conn.execute("INSERT OR REPLACE INTO robot_config (key, value) VALUES ('robot_name', 'Jarvis')")
    conn.execute("INSERT OR REPLACE INTO robot_config (key, value) VALUES ('max_linear_speed', '1.2')")
    conn.execute("INSERT OR REPLACE INTO robot_config (key, value) VALUES ('voice_gender', 'female')")
    conn.commit()
    conn.close()
    print(f"[Database Init] Created and populated {robot_db}")

    # Create logs.db
    logs_db = os.path.join(base_dir, "logs.db")
    conn_logs = sqlite3.connect(logs_db)
    conn_logs.executescript(sql_script)
    conn_logs.execute("INSERT INTO system_logs (level, module, message) VALUES ('INFO', 'SYSTEM', 'Database initialized successfully')")
    conn_logs.commit()
    conn_logs.close()
    print(f"[Database Init] Created and populated {logs_db}")

if __name__ == "__main__":
    init_databases()
