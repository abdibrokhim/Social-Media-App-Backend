from database.connections import get_connection, get_cursor

table_name = 'USERS'

def create_database():
    try:
        get_cursor().execute(f'''
                            CREATE TABLE {table_name}
                            (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255) NOT NULL,
                                image VARCHAR(255),
                                likes INT,
                                posts INT
                            );
                            ''')
        get_cursor().close()
        return True
    except Exception as e:
        print(e)
        return False
