from fastapi import APIRouter
from .auth import router as router_auth
from .test import router_protected as router_test

router = APIRouter()

router.include_router(router_auth)
router.include_router(router_test)
