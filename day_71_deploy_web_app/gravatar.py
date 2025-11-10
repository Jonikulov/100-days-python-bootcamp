import hashlib
from urllib.parse import urlencode

def get_gravatar_url(
        email: str | None = None,
        size: int = 128,
        rating: str = "g",
        default: str = "retro",
        force_default: bool = False,
    ) -> str:
    """
    Generates a Gravatar image URL for the given email address.

    Args:
        email: The email address to generate a Gravatar for, optional
        size: Avatar size in pixels [1-2048], defaults to 128
        rating: Content rating ('g', 'pg', 'r', 'x'), defaults to 'g'
        default: Default image if no Gravatar exists
                    ('404', 'mp', 'identicon', 'monsterid', 'wavatar',
                    'retro', 'robohash', 'blank'), defaults to 'retro'
        force_default: Force default image even if Gravatar exists,
                        defaults to False

    Returns:
        str: Complete Gravatar URL
    """

    # Normalize email the way Gravatar expects
    email_bytes = (email or "").strip().lower().encode("utf-8")
    # Gravatar uses MD5 of normalized email
    email_hash = hashlib.md5(email_bytes).hexdigest()
    base_url = "https://www.gravatar.com/avatar/"
    # Validate the size
    size = max(1, min(int(size), 2048))
    # Query parameters
    params = {"s": size, "d": default, "r": rating}
    if force_default:
        params["f"] = "y"

    return f"{base_url}{email_hash}?{urlencode(params)}"
