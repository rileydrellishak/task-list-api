from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from ..db import db
from typing import Optional
from datetime import datetime

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]]
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional['Goal']] = relationship(back_populates="tasks")

    @classmethod
    def from_dict(cls, task_data):
        if 'is_complete' not in task_data or task_data['is_complete'] is False:
            task_data['is_complete'] = None

        new_task = Task(
            title=task_data['title'],
            description=task_data['description'],
            completed_at=task_data['is_complete'],
            goal_id=task_data.get('goal_id', None)
            )
        
        return new_task
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'is_complete': bool(self.completed_at),
            **({'goal_id': self.goal_id} if self.goal_id else {})
        }