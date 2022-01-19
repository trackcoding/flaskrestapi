from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flaskext.mysql import MySQL
#from config import CONSTANTS
import logging
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
#Create an instance of MySQL
mysql = MySQL()

app = Flask(__name__)
api = Api(app)

#Set database credentials in config.
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'mysql'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

'''
    List the task performed by the application
'''

TASKS = {
    '1 (GetList)': 'Get all programmatic language',
    '2 (Save)': 'Save the new data',
    '3 (Update)': 'Update the author name',
    '4 (Delete)': 'Delete the language',
}


def abort_if_task_doesnt_exist(task_id):
    isPresent = False
    for key in TASKS:
        logging.info(key, task_id)
        if task_id in key:
            isPresent = True

    if isPresent == False:
        abort(404, message="Task {} doesn't exist".format(task_id))

'''
    List of data used by the application
'''

def data_exist(data_id):
    #print(str(data_id), data)
    isPresent = False
    for key in data:
        logging.info(key, data_id)
        if data_id in key:
            isPresent = True

    return isPresent

def get_file_handler():
   file_handler = TimedRotatingFileHandler("../logs/logs.log", when='midnight')
   file_handler.setFormatter(FORMATTER)
   return file_handler

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)  # better to have too much log than not enough
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


parser = reqparse.RequestParser()
parser.add_argument('id', type=str, required=False, help="Get the values")
parser.add_argument('author', type=str, required=False, help="Get the Author")
parser.add_argument('language', type=str, required=False, help="Get the Language")

'''
    GET/UPDATE/DELETE the data.
'''
class Task(Resource):
    logger = None

    def __init__(self):
        self.logger = get_logger("Task")

    def get(self, task_id):
        self.logger.info("Retrieve Language Data")
        args = parser.parse_args()
        abort_if_task_doesnt_exist(task_id)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            sqlselectquery = """select * from data.language"""
            if args['id'] and data_exist(args['id']):
                sqlselectquery = sqlselectquery +""" where id =%s """
            if args['id']:
                cursor.execute(sqlselectquery,(int(args['id'])))
            else:
                cursor.execute(sqlselectquery)
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def delete(self, task_id):
        self.logger.info("Delete Language Data")
        print("Delete data")
        args = parser.parse_args()
        abort_if_task_doesnt_exist(task_id)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            print("args",args['id'])
            if args['id']:
                deletequery = """delete from data.language where id = %s"""
                cursor.execute(deletequery, (int(args['id'])))
                conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
        return 'Deletion is successful', 204

    def put(self, task_id):
        self.logger.info("Update Language Data")
        args = parser.parse_args()
        abort_if_task_doesnt_exist(task_id)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            sql_update_query = """Update data.language set author = %s where language = %s"""
            input_data =(args['author'] , args['language'])
            cursor.execute(sql_update_query, (input_data))
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
        return '', 201


'''
    LIST all TASK and Save the new data.
'''
class TaskList(Resource):
    def get(self):
        return TASKS

    def post(self):
        self.logger.info("Add Language Data")
        args = parser.parse_args()
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            sqlselectquery = """select max(id) from data.language"""
            cursor.execute(sqlselectquery)
            data_id = cursor.fetchone()[0] + 1
            input_data =(data_id, args['author'] , args['language'])
            insert_query = """INSERT INTO data.language (id, language, author) 
                                  VALUES 
                                  (%s, %s , %s) """
            cursor.execute(insert_query , input_data)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

        return "New Language is inserted", 201


api.add_resource(TaskList, '/task')
api.add_resource(Task, '/task/<task_id>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

