import time
import uuid
import traceback
import psutil
import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from dotenv import load_dotenv

from services.ai import converse_with_assistant

load_dotenv()

# ==============================================================================
# Regra #3: Configuração do Structured JSON Logging
# ==============================================================================
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer() # Força a saída de todos os logs em formato JSON
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

app = FastAPI(title="Saas Rotina Backend", description="Hybrid AI Fitness API (MVP DevOps)")

# Configuração de CORS para permitir requisições do Web App (Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # No MVP local, liberamos tudo. Em prod: ["https://seu-app.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================================================================
# Regra #1 e #7: Middleware para Request ID único e Tracking de Tempo
# ==============================================================================
@app.middleware("http")
async def request_logger_middleware(request: Request, call_next):
    # Gera um ID único para cada requisição recebida
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    # Adiciona o request_id no contexto do log estruturado
    log = logger.bind(request_id=request_id, method=request.method, url=str(request.url.path))
    
    try:
        response = await call_next(request)
        process_time_ms = round((time.time() - start_time) * 1000, 2)
        
        # Adiciona o ID no header da resposta para rastreabilidade no cliente
        response.headers["X-Request-ID"] = request_id
        
        log.info("request_completed", status_code=response.status_code, process_time_ms=process_time_ms)
        return response
    except Exception as exc:
        process_time_ms = round((time.time() - start_time) * 1000, 2)
        # O erro real será tratado pelo Global Exception Handler, mas garantimos que a métrica de tempo seja capturada.
        raise exc

# ==============================================================================
# Regra #2: Global Exception Handler com Stack Trace Completo
# ==============================================================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Pega o Stack Trace inteiro
    tb_str = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    
    logger.error("unhandled_exception", error=str(exc), stack_trace=tb_str)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error", 
            "error": str(exc),
            # O front-end/usuário recebe o erro amigável, o Stack Trace real vai pro JSON log
            "message": "An unexpected error occurred. Please check the server logs."
        }
    )

# ==============================================================================
# Regra #4 e #7: Health Check Detalhado com Métricas de Performance
# ==============================================================================
@app.get("/health")
def health_check():
    # Obtém métricas do sistema em tempo real
    cpu_usage = psutil.cpu_percent(interval=None)
    memory_info = psutil.virtual_memory()
    
    health_data = {
        "status": "healthy",
        "service": "Saas Rotina Backend",
        "metrics": {
            "cpu_usage_percent": cpu_usage,
            "memory_usage_percent": memory_info.percent,
            "memory_available_mb": round(memory_info.available / (1024 * 1024), 2)
        }
    }
    
    logger.info("health_check_ping", **health_data)
    return health_data

# ==============================================================================
# Endpoints do Agente Conversacional
# ==============================================================================
class ChatRequest(BaseModel):
    message: str
    history: list = [] # Lista de {"role": "...", "content": "..."}

@app.post("/api/chat")
def chat_with_assistant(request: ChatRequest):
    # Envia o histórico e a nova mensagem para o Claude
    response_data = converse_with_assistant(request.history, request.message)
    
    # Opcional: Se 'extracted_data' tiver dados novos (como peso), aqui nós chamaríamos
    # o database.py para fazer o UPSERT no Supabase.
    
    return response_data.model_dump()
