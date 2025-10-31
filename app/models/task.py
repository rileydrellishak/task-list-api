from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from typing import Optional
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    @classmethod
    def from_dict(cls, task_data):
        if 'is_complete' not in task_data.keys():
            task_data['is_complete'] = None

        if task_data['is_complete'] is False:
            task_data['is_complete'] = None

        new_task = Task(
            title=task_data['title'],
            description=task_data['description'],
            completed_at=task_data['is_complete']
            )
        
        return new_task
    
    def to_dict(self):
        task_dict = {}

        if self.completed_at is None:
            task_dict['is_complete'] = False
        
        task_dict['id'] = self.id
        task_dict['title'] = self.title
        task_dict['description'] = self.description

        return task_dict