from fastapi import APIRouter

from . import actu_ia

router = APIRouter()
router.include_router(actu_ia.router, prefix="/actu_ia", tags=["actu_ia"])
