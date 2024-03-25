import os
from dotenv import load_dotenv

load_dotenv()

if os.getenv('DATABASE_ENGINE') == 'django.db.backends.mysql':
    import pymysql
    pymysql.install_as_MySQLdb()