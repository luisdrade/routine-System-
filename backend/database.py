import os
import time
import structlog
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

logger = structlog.get_logger()

# Inicialização do Supabase Client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    logger.warning("supabase_credentials_missing", message="Certifique-se de configurar SUPABASE_URL e SUPABASE_SERVICE_ROLE_KEY no .env")

# O Service Role Key nos dá acesso para contornar RLS em operações back-end, mas 
# manteremos as verificações lógicas no app e usaremos o JWT do usuário no futuro.
supabase: Client = create_client(SUPABASE_URL or "", SUPABASE_KEY or "")

# ==============================================================================
# Regra #5: DB Query Logging com tempo
# ==============================================================================
class DBLoggingWrapper:
    """
    Um wrapper simples para interceptar chamadas ao Supabase,
    medir o tempo de execução e gerar logs estruturados (Regra 5).
    """
    
    @staticmethod
    def execute_query(query_func, query_name: str, **kwargs):
        start_time = time.time()
        try:
            result = query_func(**kwargs)
            process_time_ms = round((time.time() - start_time) * 1000, 2)
            
            logger.info(
                "db_query_success", 
                query=query_name, 
                process_time_ms=process_time_ms,
                # Não logamos o resultado inteiro para não poluir ou vazar dados no log
            )
            return result
        except Exception as exc:
            process_time_ms = round((time.time() - start_time) * 1000, 2)
            logger.error(
                "db_query_error", 
                query=query_name, 
                error=str(exc), 
                process_time_ms=process_time_ms
            )
            raise exc

db = DBLoggingWrapper()
