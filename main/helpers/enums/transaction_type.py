from enum import Enum


class TransactionType(Enum):
    DEBIT_SPIN = "DEBIT_SPIN"  # Custo do giro da roleta
    CREDIT_PRIZE = "CREDIT_PRIZE"  # Ganho da roleta
    DEPOSIT = "DEPOSIT"  # Depósito de fundos pelo usuário
    WITHDRAW = "WITHDRAW"  # Saque de fundos pelo usuário
    CORRECTION = "CORRECTION"  # Ajuste manual ou administrativo
