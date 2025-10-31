from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    
    except:
        response = {'message': f'{cls.__name__} {model_id} invalid'}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {'message': f'{cls.__name__} {model_id} not found'}
        abort(make_response(response, 404))

    return model

def create_instance(cls, data):
    pass

# create an instance of model_class
# for each key, value in data_dict:
#     if the key corresponds to a valid model attribute:
#         set that attribute on the instance
# handle any special-case logic (like completed_at)
# return the instance

# involves dir() and __dir__ for the class definition. dir() returns a list of the object's attributes, and __dir__ within class definition lets us customize output of dir(). will save this for later wave when I make the goal model.