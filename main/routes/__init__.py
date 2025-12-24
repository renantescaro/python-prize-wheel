from fastapi import APIRouter
from .auth import router as router_auth
from .client.campaign import router as router_campaign
from .client.client_account import router as router_client_account
from .client.client import router as router_client
from .client.test_client import router_protected as router_test_client
from .client.prize_wheel import router_protected as router_prize_wheel

from .user.campaign import router as router_admin_campaign
from .user.client import router as router_admin_client
from .user.company import router_protected as router_company
from .user.dashboard import router_protected as router_dashboard
from .user.test_user import router_protected as router_test_user
from .user.user import router_protected as router_user
from .user.spin import router_protected as router_spin
from .user.transactions import router_protected as router_transaction

router = APIRouter()

router.include_router(router_auth)
router.include_router(router_client_account)
router.include_router(router_admin_campaign)
router.include_router(router_admin_client)
router.include_router(router_company)
router.include_router(router_campaign)
router.include_router(router_client)
router.include_router(router_dashboard)
router.include_router(router_prize_wheel)
router.include_router(router_test_client)
router.include_router(router_test_user)
router.include_router(router_user)
router.include_router(router_spin)
router.include_router(router_transaction)
