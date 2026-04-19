from sqlalchemy.orm import Session
from .models import ChatSession, ChatMessage

def get_or_create_session(db: Session, session_id: str):
    session = db.query(ChatSession).filter_by(session_id=session_id).first()
    if not session:
        session = ChatSession(session_id=session_id)
        db.add(session)
        db.commit()
    return session

def save_message(db: Session, session_id: str, role: str, content: str):
    msg = ChatMessage(session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()

def get_history(db: Session, session_id: str):
    return db.query(ChatMessage).filter_by(
        session_id=session_id
    ).order_by(ChatMessage.timestamp).all()