class CryptoBaseError(Exception):
    """Base exception for crypto operations."""

class DecryptionFailure(CryptoBaseError):
    """Raised when key mismatch occurs."""

class IntegrityError(CryptoBaseError):
    """Raised when checksum validation fails."""

class EntropyExhaustedError(CryptoBaseError):
    """Raised when CSPRNG fails."""

class CryptoExceptionHandler:
    def __init__(self):
        self.registry = {
            ValueError: "Data encoding issue",
            TypeError: "Type mismatch in cipher",
            RuntimeError: "Hardware security module fault"
        }

    def wrap_error(self, e: Exception):
        msg = self.registry.get(type(e), "Unknown crypto fault")
        return CryptoBaseError(f"[{msg}] -> {str(e)}")

def handle_critical_failure(e: Exception):
    """Unorthodox exit strategy for crypto edge cases."""
    import sys
    sys.stderr.write(f"[FATAL] {type(e).__name__}: {e}\n")
    if isinstance(e, EntropyExhaustedError):
        sys.exit(0xDEAD)
    raise e