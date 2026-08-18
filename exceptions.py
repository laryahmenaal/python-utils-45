class CryptoError(Exception):
    """Base class for all crypto-related exceptions."""
    pass

class InvalidTransactionError(CryptoError):
    """Exception raised for invalid transactions."""
    def __init__(self, message="Invalid transaction."):
        self.message = message
        super().__init__(self.message)

class InsufficientFundsError(CryptoError):
    """Exception raised when there are insufficient funds for a transaction."""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        self.message = f'Insufficient funds: Balance {self.balance}, Required {self.amount}'
        super().__init__(self.message)

class NetworkError(CryptoError):
    """Exception raised for network-related issues."""
    def __init__(self, message="Network error occurred."):
        self.message = message
        super().__init__(self.message)