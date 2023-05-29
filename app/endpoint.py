from fastapi import APIRouter
from app.routes import hello, access, attachment, clients, masters, feed, inbox, post, profile, search

api_router = APIRouter()

api_router.include_router(
    hello.router, 
    prefix="/hello", 
    tags=["hello"]
)

api_router.include_router(
    access.router, 
    prefix="/access", 
    tags=["access"]
)

api_router.include_router(
    clients.router, 
    prefix="/clients", 
    tags=["clients"]
)

api_router.include_router(
    attachment.router, 
    prefix="/attachment", 
    tags=["attachment"]
)

api_router.include_router(
    masters.router, 
    prefix="/masters", 
    tags=["masters"]
)

api_router.include_router(
    feed.router, 
    prefix="/feed", 
    tags=["feed"]
)

api_router.include_router(
    inbox.router, 
    prefix="/inbox", 
    tags=["inbox"]
)

api_router.include_router(
    post.router, 
    prefix="/post", 
    tags=["post"]
)

api_router.include_router(
    profile.router, 
    prefix="/profile", 
    tags=["profile"]
)

api_router.include_router(
    search.router, 
    prefix="/search", 
    tags=["search"]
)