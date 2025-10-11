from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Upload(Base):
    __tablename__ = "uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # 'docx' or 'pdf'
    file_size = Column(Integer, nullable=False)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    jobs = relationship("Job", back_populates="upload")
    reports = relationship("Report", back_populates="upload")


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(Integer, ForeignKey("uploads.id"), nullable=False)
    task_id = Column(Integer, nullable=False)  # Task index from parsed file
    question_text = Column(Text, nullable=False)
    code_snippet = Column(Text, nullable=False)
    theme = Column(String, nullable=False, default="idle")  # 'idle' or 'vscode'
    status = Column(String, nullable=False, default="pending")  # pending, running, completed, failed
    output_text = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    execution_time = Column(Integer, nullable=True)  # milliseconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    upload = relationship("Upload", back_populates="jobs")
    screenshots = relationship("Screenshot", back_populates="job")


class Screenshot(Base):
    __tablename__ = "screenshots"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    job = relationship("Job", back_populates="screenshots")


class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(Integer, ForeignKey("uploads.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    screenshot_order = Column(JSON, nullable=True)  # Array of job IDs in order
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    upload = relationship("Upload", back_populates="reports")


class AIJob(Base):
    __tablename__ = "ai_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    upload_id = Column(Integer, ForeignKey("uploads.id"), nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending, running, completed, failed
    theme = Column(String, nullable=False, default="idle")  # 'idle' or 'vscode'
    insertion_preference = Column(String, nullable=False, default="below_question")  # below_question, bottom_of_page
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    upload = relationship("Upload")
    tasks = relationship("AITask", back_populates="job", cascade="all, delete-orphan")


class AITask(Base):
    __tablename__ = "ai_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("ai_jobs.id"), nullable=False)
    task_id = Column(String, nullable=False)  # Unique identifier for the task
    task_type = Column(String, nullable=False)  # screenshot_request, answer_request, code_execution
    question_context = Column(Text, nullable=False)
    suggested_code = Column(Text, nullable=True)
    user_code = Column(Text, nullable=True)  # User-edited code
    extracted_code = Column(Text, nullable=True)  # Code from document
    assistant_answer = Column(Text, nullable=True)
    confidence = Column(Integer, nullable=False)  # 0-100
    suggested_insertion = Column(String, nullable=False, default="below_question")
    brief_description = Column(Text, nullable=True)
    follow_up = Column(Text, nullable=True)
    follow_up_answer = Column(Text, nullable=True)  # User's answer to follow-up
    status = Column(String, nullable=False, default="pending")  # pending, running, completed, failed
    screenshot_path = Column(String, nullable=True)
    stdout = Column(Text, nullable=True)
    exit_code = Column(Integer, nullable=True)
    caption = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    job = relationship("AIJob", back_populates="tasks")
