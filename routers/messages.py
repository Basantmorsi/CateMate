from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, or_
from CateMate.models.message import Message
from CateMate.models.owner import Owner, AllowedGender
from CateMate.schemas.message import MessageCreate, MessageRead
from CateMate.utils.auth import get_current_user
from CateMate.db import SessionDep

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("/", response_model=list[MessageRead], status_code=status.HTTP_200_OK)
def get_messages(session: SessionDep, owner_id: int = Depends(get_current_user)):
    # Every message the current user is part of, newest first.
    messages = session.exec(
        select(Message)
        .where(or_(Message.sender_id == owner_id, Message.recipient_id == owner_id))
        .order_by(Message.created_at.desc())
    ).all()
    return messages


@router.post("/", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
def send_message(data: MessageCreate, session: SessionDep, owner_id: int = Depends(get_current_user)):
    owner_id = int(owner_id)
    if data.recipient_id == owner_id:
        raise HTTPException(status_code=400, detail="You cannot message yourself")

    sender = session.get(Owner, owner_id)
    recipient = session.get(Owner, data.recipient_id)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    # Respect the recipient's messaging privacy preference.
    if recipient.allow_message_from == AllowedGender.B and sender.gender != recipient.gender:
        raise HTTPException(
            status_code=403,
            detail="This owner only accepts messages from owners of the same gender",
        )

    message = Message(
        sender_id=owner_id,
        recipient_id=data.recipient_id,
        cat_id=data.cat_id,
        content=data.content,
    )
    try:
        session.add(message)
        session.commit()
        session.refresh(message)
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to send message")

    return message
