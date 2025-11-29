# blog_app/schemas/schemas_law.py

from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# --- Public/Frontend Schemas (Read Only) ---

class LawBlogTopicRequest(BaseModel):
    topic: str
    # Removed 'generate' bool as frontend cannot trigger generation

class MoreBlogsRequest(BaseModel):
    topic: str
    existing_titles: List[str]
    # Removed 'generate' bool

class AllCategoriesRequest(BaseModel):
    categories: List[str]
    # Removed 'generate' bool

class GeneratedBlog(BaseModel):
    id: int
    title: str
    content: str
    createdAt: datetime

    model_config = ConfigDict(from_attributes=True)

class LawBlogResponse(BaseModel):
    blogs: List[GeneratedBlog]

# --- Admin Schemas (Write/Generate) ---

class AdminGenerateRequest(BaseModel):
    topic: str
    # Optional: override how many to generate, default handled in backend
    count: int = 3 

class AdminDeleteResponse(BaseModel):
    success: bool
    message: str