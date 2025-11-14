def normalize_sku(sku: str) -> str:
    """
    Convert SKU into a clean, normalized, case-insensitive value.
    This ensures consistent uniqueness in the database.
    """
    if not sku:
        return ""

    return sku.strip().lower()
