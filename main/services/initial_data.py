from typing import Optional
from main.database.database import Database, select
from main.database.models.company_model import Company
from main.database.models.user_model import User
from main.helpers.enums.dot_env import DotEnvEnum
from main.helpers.settings import Settings
from main.services.auth.password_hash import PasswordHash


class InitialData:
    def execute(self):
        if not self._empty_database():
            return

        company_id = self._insert_adm_company()
        self._insert_adm_user(company_id=company_id)

    def _empty_database(self) -> bool:
        sql = select(Company)
        company: Optional[Company] = Database().get_one(sql)

        if company:
            return False

        return True

    def _insert_adm_company(self):
        adm_company = Company(
            name="adm",
            tenant="adm",
        )
        company: Optional[Company] = Database().save(
            adm_company,
            refresh=True,
        )
        if company:
            return company.id

        raise Exception("Error create company")

    def _insert_adm_user(self, company_id: int):
        USER_ADM = Settings.get(
            DotEnvEnum.USER_ADM,
        )
        USER_ADM_PASSWORD = Settings.get(
            DotEnvEnum.USER_ADM_PASSWORD,
        )
        password = PasswordHash().execute(USER_ADM_PASSWORD)

        adm_user = User(
            company_id=company_id,
            name=USER_ADM,
            password=password,
            is_active=True,
        )
        Database().save(adm_user)
