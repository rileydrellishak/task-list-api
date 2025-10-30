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
        new_task = Task(title=task_data['title'],
                        description=task_data['description'],
                        completed_at=task_data['completed_at'])
        
        return new_task