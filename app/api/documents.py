"""Document upload and management endpoints."""

from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app import database
from app.core.permissions import Role
from app.models.document import Document
from app.api.deps import get_current_roles

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def upload_document(
    registration_id: int | None = None,
    student_id: int | None = None,
    parent_id: int | None = None,
    file: UploadFile = File(..., description="Document file"),
    current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    """Upload a document and store it securely on disk."""
    uploads_dir = Path("app/uploads")
    uploads_dir.mkdir(parents=True, exist_ok=True)

    # Generate a safe storage key (UUID prefix + original extension)
    ext = Path(file.filename or "file").suffix.lower()
    storage_key = f"{uuid4().hex}{ext}"

    # Save file securely
    file_path = uploads_dir / storage_key
    contents = await file.read()
    file_path.write_bytes(contents)

    doc = Document(
        original_filename=file.filename,
        filename=storage_key,
        file_type=file.content_type or "application/octet-stream",
        file_size=len(contents),
        storage_key=str(file_path),
        registration_id=registration_id,
        student_id=student_id,
        parent_id=parent_id,
        document_type="other",
        is_verified=False,
        is_deleted=False,
    )
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        session.add(doc)
        await session.commit()
        await session.refresh(doc)
    return doc


@router.get("", response_model=List[Document])
async def list_documents(
    registration_id: int | None = None,
    student_id: int | None = None,
    parent_id: int | None = None,
    current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        query = select(Document).where(Document.is_deleted == False)  # noqa: E712
        if registration_id:
            query = query.where(Document.registration_id == registration_id)
        if student_id:
            query = query.where(Document.student_id == student_id)
        if parent_id:
            query = query.where(Document.parent_id == parent_id)
        result = await session.execute(query)
        return result.scalars().all()


@router.get("/{document_id}")
async def get_document(
    document_id: int,
    current_user = Depends(get_current_roles(["admin", "receptionist", "registration_officer"])),
):
    from app.database import AsyncSessionLocal
    async with AsyncSessionLocal() as session:
        stmt = select(Document).where(Document.id == document_id)
        result = await session.execute(stmt)
        doc = result.scalar_one_or_none()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        return doc
