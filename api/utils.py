"""
The utils library aims to extend the module's functionality.
"""

import time

def is_valid_token(token):
    """Verifies if the token will expires in a future point in time.
        Args:
            token:
        Returns:
            A boolean value
    """
    return token['expires_at'] > time.time()
