from flask import abort, make_response, request
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

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    
    except KeyError as error:
        response = {'details': f'Invalid data'}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attr, value in filters.items():
            if hasattr(cls, attr):
                query = query.where(getattr(cls, attr).ilike(f'%{value}%'))

            elif attr == 'sort':
                if value == 'desc':
                    query = query.order_by(cls.title.desc())
                else:
                    query = query.order_by(cls.title)
    
    models = db.session.scalars(query)
    models_response = [model.to_dict() for model in models]
    return models_response