import os
from pymongo import MongoClient
import pymysql
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class MongoConnector:
    """MongoDB connection handler"""
    
    def __init__(self):
        self.host = os.getenv('MONGO_HOST')
        self.port = int(os.getenv('MONGO_PORT', 27017))
        self.database = os.getenv('MONGO_DB')
        self.username = os.getenv('MONGO_USER')
        self.password = os.getenv('MONGO_PASS')
        self.client = None
        self.db = None
    
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            connection_string = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}"
            self.client = MongoClient(connection_string)
            self.db = self.client[self.database]
            print(f"✓ Connected to MongoDB: {self.database}")
            return self.db
        except Exception as e:
            print(f"✗ MongoDB connection failed: {e}")
            raise
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✓ MongoDB connection closed")


class MySQLConnector:
    """MySQL connection handler"""
    
    def __init__(self):
        self.host = os.getenv('MYSQL_HOST')
        self.port = int(os.getenv('MYSQL_PORT', 3306))
        self.database = os.getenv('MYSQL_DB')
        self.username = os.getenv('MYSQL_USER')
        self.password = os.getenv('MYSQL_PASS')
        self.connection = None
    
    def connect(self):
        """Establish connection to MySQL"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"✓ Connected to MySQL: {self.database}")
            return self.connection
        except Exception as e:
            print(f"✗ MySQL connection failed: {e}")
            raise
    
    def close(self):
        """Close MySQL connection"""
        if self.connection:
            self.connection.close()
            print("✓ MySQL connection closed")


class RedshiftConnector:
    """Redshift connection handler using SQLAlchemy"""
    
    def __init__(self):
        self.host = os.getenv('REDSHIFT_HOST')
        self.port = int(os.getenv('REDSHIFT_PORT', 5439))
        self.database = os.getenv('REDSHIFT_DB')
        self.username = os.getenv('REDSHIFT_USER')
        self.password = os.getenv('REDSHIFT_PASS')
        self.engine = None
    
    def connect(self):
        """Establish connection to Redshift"""
        try:
            connection_string = (
                f"postgresql+psycopg2://{self.username}:{self.password}"
                f"@{self.host}:{self.port}/{self.database}"
            )
            self.engine = create_engine(connection_string)
            # Test connection
            with self.engine.connect() as conn:
                conn.execute("SELECT 1")
            print(f"✓ Connected to Redshift: {self.database}")
            return self.engine
        except Exception as e:
            print(f"✗ Redshift connection failed: {e}")
            raise
    
    def close(self):
        """Close Redshift connection"""
        if self.engine:
            self.engine.dispose()
            print("✓ Redshift connection closed")


# Test connections
if __name__ == "__main__":
    print("Testing database connections...\n")
    
    # Test MongoDB
    try:
        mongo = MongoConnector()
        mongo.connect()
        mongo.close()
    except Exception as e:
        print(f"MongoDB test failed: {e}")
    
    print()
    
    # Test MySQL
    try:
        mysql = MySQLConnector()
        mysql.connect()
        mysql.close()
    except Exception as e:
        print(f"MySQL test failed: {e}")
    
    print()
    
    # Test Redshift
    try:
        redshift = RedshiftConnector()
        redshift.connect()
        redshift.close()
    except Exception as e:
        print(f"Redshift test failed: {e}")
