from memory.database import SessionLocal
from memory.models import Conversation


def save_message(session_id, role, message):
    db = SessionLocal()
    try:
        convo = Conversation(
            session_id=session_id,
            role=role,
            message=message
        )
        db.add(convo)
        db.commit()
    finally:
        db.close()


def get_conversation_history(session_id, limit=20):
    db = SessionLocal()
    try:
        messages = (
            db.query(Conversation)
            .filter(Conversation.session_id == session_id)
            .order_by(Conversation.created_at.asc())
            .limit(limit)
            .all()
        )
        return messages
    finally:
        db.close()