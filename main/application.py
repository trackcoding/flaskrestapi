from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
#from config import CONSTANTS
import logging
from logging.handlers import TimedRotatingFileHandler

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

app = Flask(__name__)
api = Api(app)

TASKS = {
    '1 (GetList)': 'Get all programmatic language',
    '2 (Save)': 'Save the new data',
    '3 (Update)': 'Update the author name',
    '4 (Delete)': 'Delete the language',
}

data = {
    "ID1": {"Languages": "Python", "Author": "Guido van Rossum"},
    "ID2": {"Languages": "Angular", "Author": "Deborah Kurata"},
    "ID3": {"Languages": "Perl", "Author": "Larry Arnold Wall"}
}

'''
    List the task performed by the application
'''

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
    print('logging')
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
    def __init__(self):
        logger = get_logger("Task")

    def get(self, task_id):
        logger = get_logger("Task")
        logger.info("Retrieve Language Data")
        args = parser.parse_args()
        abort_if_task_doesnt_exist(task_id)
        if args['id'] and data_exist(args['id']):
            id = args['id']
            return data["ID" + id]
        return data

    def delete(self, task_id):
        args = parser.parse_args()
        abort_if_task_doesnt_exist(task_id)
        if args['id'] and data_exist(args['id']):
            id = args['id']
            del data["ID" + id]
        return '', 204

    def put(self, task_id):
        args = parser.parse_args()
        abort_if_task_doesnt_exist(task_id)
        if args['id'] and data_exist("ID" + args['id']):
            id = args['id']
            data["ID" + id]['Author'] = args['author']
        return '', 201


'''
    LIST all TASK and Save the new data.
'''
class TaskList(Resource):
    def get(self):
        return TASKS

    def post(self):
        args = parser.parse_args()
        data_id = int(max(data.keys()).lstrip('ID')) + 1
        data_id = 'ID' + str(data_id)
        data[data_id] = {"Language": args['language'], "Author": args['author']}
        return data[data_id], 201


api.add_resource(TaskList, '/task')
api.add_resource(Task, '/task/<task_id>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

