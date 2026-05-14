import time
import uuid
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import logger
import traceback

class GlobalExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Add request ID to logger context if needed
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id
            
            logger.info(f"Request {request_id} completed in {process_time:.4f}s: {request.method} {request.url.path}")
            return response
            
        except HTTPException as http_exc:
            logger.warning(f"HTTP Exception {request_id}: {http_exc.detail}")
            return JSONResponse(
                status_code=http_exc.status_code,
                content={"error": http_exc.detail, "request_id": request_id}
            )
        except Exception as e:
            logger.error(f"Unhandled Exception {request_id}: {str(e)}\n{traceback.format_exc()}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred. Please contact support.",
                    "request_id": request_id
                }
            )
