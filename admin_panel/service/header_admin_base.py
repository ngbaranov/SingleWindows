from fastapi import Request

async def header_admin(request: Request, address: str = "admin_panel/"):
    base_url = str(request.base_url)
    is_admin = request.headers.get("Referer", "").startswith(f"{base_url}{address}")
    return is_admin