import os
import sys
import django
from django.conf import settings
import MySQLdb

def main():
    """
    Connects to the MySQL server and creates the database specified in settings.py
    if it doesn't already exist.
    """
    # Point to the project's settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_system.settings')
    
    # This is required to access Django settings outside of a manage.py command
    django.setup()

    # Get database configuration from Django settings
    db_config = settings.DATABASES['default']
    db_name = db_config.get('NAME')
    db_user = db_config.get('USER')
    db_password = db_config.get('PASSWORD')
    db_host = db_config.get('HOST')
    db_port = db_config.get('PORT')

    if not db_name:
        print("Database name not configured in settings.py. Aborting.")
        sys.exit(1)

    print("--- Starting Database Check ---")
    
    try:
        # Connect to the MySQL server (without specifying a database)
        conn = MySQLdb.connect(
            host=db_host,
            user=db_user,
            passwd=db_password,
            port=int(db_port) if db_port else 3306
        )
        cursor = conn.cursor()

        # Execute the SQL command to create the database if it doesn't exist
        # Using "IF NOT EXISTS" makes the script safe to run multiple times.
        print(f"Ensuring database '{db_name}' exists...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
        print(f"Success: Database '{db_name}' is ready.")

    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL or creating the database: {e}")
        sys.exit(1)
        
    finally:
        # Clean up the connection
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        print("--- Database Check Complete ---")


if __name__ == '__main__':
    # Add the backend directory to the Python path to allow Django imports
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()

