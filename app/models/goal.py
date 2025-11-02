from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from typing import Optional
from datetime import datetime

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(
            title=goal_data['title']
            )
        
        return new_goal
    
    def to_dict(self):
        goal_dict = {}
        
        goal_dict['id'] = self.id
        goal_dict['title'] = self.title

        return goal_dict