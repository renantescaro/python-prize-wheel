from fastapi import APIRouter
from .auth import router as router_auth
from .client import router as router_client
from .company import router_protected as router_company
from .dashboard import router_protected as router_dashboard
from .test_client import router_protected as router_test_client
from .test_user import router_protected as router_test_user
from .user import router_protected as router_user

router = APIRouter()

router.include_router(router_auth)
router.include_router(router_client)
router.include_router(router_company)
router.include_router(router_dashboard)
router.include_router(router_test_client)
router.include_router(router_test_user)
router.include_router(router_user)
