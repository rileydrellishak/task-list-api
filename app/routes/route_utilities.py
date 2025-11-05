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
        sort_by = filters.get('sort_by', 'title')
        direction = filters.get('sort', None)

        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

        if hasattr(cls, sort_by):
            sort_column = getattr(cls, sort_by)
            if direction == 'desc':
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column)
    
    else:
        query = query.order_by(cls.title)

    models = db.session.scalars(query)
    models_response = [model.to_dict() for model in models]
    return models_response