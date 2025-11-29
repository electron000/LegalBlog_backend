# blog_app/services/crud_law.py

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import models_law
from ..schemas import schemas_law 
from typing import List, Optional, Sequence

# ==========================================
# PUBLIC / FRONTEND CRUD
# ==========================================

async def get_all_blogs(db: AsyncSession) -> Sequence[models_law.GeneratedLawBlog]:
    """
    Fetches ALL blogs from the database.
    Ordered by newest first (descending).
    """
    query = (
        select(models_law.GeneratedLawBlog)
        .order_by(models_law.GeneratedLawBlog.createdAt.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()

# ==========================================
# ADMIN / HELPER CRUD
# ==========================================

async def get_blog_by_id(db: AsyncSession, blog_id: int) -> Optional[models_law.GeneratedLawBlog]:
    """
    Used by Admin Delete to find the blog before deleting.
    """
    result = await db.execute(
        select(models_law.GeneratedLawBlog).where(models_law.GeneratedLawBlog.id == blog_id)
    )
    return result.scalars().first()

async def create_generated_blog(
    db: AsyncSession, 
    blog: schemas_law.GeneratedBlog, 
    topic: str
) -> Optional[models_law.GeneratedLawBlog]:
    """
    Used by Admin Generate to save new AI content.
    """
    # Check if title already exists to prevent duplicates
    existing_blog_check = await db.execute(
        select(models_law.GeneratedLawBlog).where(models_law.GeneratedLawBlog.title == blog.title)
    )
    if existing_blog_check.scalars().first():
        return None
        
    new_blog = models_law.GeneratedLawBlog(
        search_topic=topic,
        title=blog.title,
        content=blog.content
    )
    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog)
    return new_blog

async def delete_blog(db: AsyncSession, blog_id: int) -> bool:
    """
    Used by Admin Delete.
    """
    blog = await get_blog_by_id(db, blog_id)
    if blog:
        await db.delete(blog)
        await db.commit()
        return True
    return False