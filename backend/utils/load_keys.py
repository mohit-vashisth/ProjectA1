from backend.core import config
from backend.utils.logger import init_logger

def load_keys():
    try:
        init_logger(message="Loading Keys from Environment Variables")
        PRIVATE_KEY, PUBLIC_KEY = config.read_pv_key()
        init_logger(message="Key Loaded successfully...")

        if not PRIVATE_KEY or not PUBLIC_KEY:
            init_logger(message="Private/Public key not loaded properly", level="critical")
            raise RuntimeError("Private/Public key not loaded properly")
        
        return PRIVATE_KEY, PUBLIC_KEY
    
    except Exception as e:
        init_logger(message=f"Error loading private/public keys: {str(e)}", level="critical")
        raise RuntimeError("Failed to initialize JWT keys") from e
