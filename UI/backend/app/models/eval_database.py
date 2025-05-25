from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class EvalTask(Base):
    __tablename__ = "eval_task"
    id = Column(Integer, primary_key=True, index=True)
    user_upload_filename = Column(String, index=True)
    stored_filename = Column(String, index=True)
    task_id = Column(String, index=True)
    file_path = Column(String, index=True)
    scenario = Column(Integer, index=True)
    workflow = Column(Integer, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<EvalTask(id={self.id}, user_upload_filename={self.user_upload_filename}, stored_filename={self.stored_filename}, task_id={self.task_id}, scenario={self.scenario}, workflow={self.workflow})>"