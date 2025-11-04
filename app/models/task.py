from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional['Goal']] = relationship(back_populates="tasks")

    @classmethod
    def from_dict(cls, task_data):
        if 'is_complete' not in task_data.keys() or task_data['is_complete'] is False:
            task_data['is_complete'] = None

        new_task = Task(
            title=task_data['title'],
            description=task_data['description'],
            completed_at=task_data['is_complete'],
            goal_id=task_data.get('goal_id', None)
            )
        
        return new_task
    
    def to_dict(self):
        task_dict = {}

        if self.completed_at is None:
            task_dict['is_complete'] = False

        if self.goal_id:
            task_dict['goal_id'] = self.goal_id

        task_dict['id'] = self.id
        task_dict['title'] = self.title
        task_dict['description'] = self.description

        return task_dict