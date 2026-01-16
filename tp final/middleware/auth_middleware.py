from fastapi import Request, HTTPException, Header
from typing import Optional
import json

def get_current_user(x_user_role: Optional[str] = Header(None), 
                     x_user_name: Optional[str] = Header(None)) -> dict:
    if not x_user_role or not x_user_name:
        raise HTTPException(status_code=401, detail="Unauthorized - No user credentials")
    
    return {"role": x_user_role, "username": x_user_name}
class AuthMiddleware:
    
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
            
        headers = dict(scope.get("headers", []))
        
        user_role = b""
        user_name = b""
        
        for key, value in headers.items():
            if key.lower() == b"x-user-role":
                user_role = value
            elif key.lower() == b"x-user-name":
                user_name = value
        
        user_role = user_role.decode("utf-8")
        user_name = user_name.decode("utf-8")
        
        if user_role and user_name:
            scope["user"] = {
                "role": user_role,
                "username": user_name
            }
        
        if scope["path"] in ["/", "/login"] or not scope["path"].startswith("/api"):
            await self.app(scope, receive, send)
            return
            
        try:
            if not user_role or not user_name:
                await self._send_error_response(send, 401, "Unauthorized - Missing user credentials")
                return
            
        except Exception as e:
            await self._send_error_response(send, 401, f"Authentication error: {str(e)}")
            return
            
        await self.app(scope, receive, send)
    
    async def _send_error_response(self, send, status_code: int, detail: str):
        """إرسال رسالة خطأ"""
        await send({
            "type": "http.response.start",
            "status": status_code,
            "headers": [(b"content-type", b"application/json")],
        })
        await send({
            "type": "http.response.body",
            "body": json.dumps({"detail": detail}).encode("utf-8"),
        })