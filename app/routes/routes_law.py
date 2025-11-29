# blog_app/routes/routes_law.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..services import utils_law, crud_law, database
from ..schemas.schemas_law import (
    LawBlogResponse, 
    GeneratedBlog,
    AdminGenerateRequest,
    AdminDeleteResponse
)
import asyncio
from datetime import datetime

router = APIRouter(prefix="/api/law-generator", tags=["Indian Law Blog Generator"])

# ==========================================
# PUBLIC / FRONTEND ROUTES
# ==========================================

@router.get("/all-blogs", response_model=LawBlogResponse)
async def get_all_blogs(db: AsyncSession = Depends(database.get_db)):
    """
    Single Entry Point for User: Fetches ALL generated blogs.
    Frontend handles filtering, searching, and pagination.
    """
    all_blogs = await crud_law.get_all_blogs(db)
    # Using from_orm to convert SQLAlchemy models to Pydantic models
    return LawBlogResponse(blogs=[GeneratedBlog.from_orm(b) for b in all_blogs])

# ==========================================
# ADMIN ROUTES (WRITE / GENERATE / DELETE)
# ==========================================

@router.post("/admin/generate", response_model=LawBlogResponse)
async def admin_generate_blogs(request: AdminGenerateRequest, db: AsyncSession = Depends(database.get_db)):
    """
    Triggers AI generation for a specific topic or 'trending'.
    This is the ONLY endpoint that calls the LLM.
    """
    generated_blogs = []
    
    # --- SCENARIO A: Generate Trending News ---
    if request.topic.lower() in ["trending", "latest news"]:
        news_titles = await utils_law.get_latest_law_news_topics()
        
        if not news_titles:
             raise HTTPException(status_code=503, detail="AI Service failed to fetch news topics.")
        
        # Limit generation based on request or default to 6 for trending
        count = request.count if request.count > 0 else 6
        
        for title in news_titles[:count]:
            # Generate content
            content = await utils_law.generate_law_blog_from_title(title)
            
            # Save to DB
            blog_schema_stub = GeneratedBlog(id=0, title=title, content=content, createdAt=datetime.now())
            created_model = await crud_law.create_generated_blog(db, blog=blog_schema_stub, topic="trending_cache")
            
            if created_model:
                generated_blogs.append(GeneratedBlog.from_orm(created_model))
            else:
                pass
                
            await asyncio.sleep(1.5) # Rate limit protection for AI API
            
        return LawBlogResponse(blogs=generated_blogs)

    # --- SCENARIO B: Generate Specific Topic/Category ---
    
    # 1. Validate Topic relevance
    if not await utils_law.is_topic_indian_law(request.topic):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Topic is not related to Indian law.")

    # 2. Generate Titles
    new_titles = await utils_law.get_related_blog_ideas(topic=request.topic, count=request.count, existing_titles=[])
    
    if not new_titles:
        raise HTTPException(status_code=503, detail="AI Service failed to generate blog ideas.")
    
    # 3. Generate Content & Save
    for title in new_titles:
        content = await utils_law.generate_law_blog_from_title(title)
        
        blog_schema_stub = GeneratedBlog(id=0, title=title, content=content, createdAt=datetime.now())
        created_blog_model = await crud_law.create_generated_blog(db, blog=blog_schema_stub, topic=request.topic)
        
        if created_blog_model:
            generated_blogs.append(GeneratedBlog.from_orm(created_blog_model))
        
        await asyncio.sleep(1.5)
        
    return LawBlogResponse(blogs=generated_blogs)


@router.delete("/admin/blog/{blog_id}", response_model=AdminDeleteResponse)
async def admin_delete_blog(blog_id: int, db: AsyncSession = Depends(database.get_db)):
    """
    Deletes a specific blog post.
    """
    success = await crud_law.delete_blog(db, blog_id)
    if not success:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    return AdminDeleteResponse(success=True, message=f"Blog {blog_id} deleted successfully.")