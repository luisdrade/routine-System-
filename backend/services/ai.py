import os
import json
import httpx
import base64
import structlog
from anthropic import Anthropic
from dotenv import load_dotenv

from models.schemas import ChatResponseSchema, PhysiqueAnalysisSchema

load_dotenv()
logger = structlog.get_logger()

# ==============================================================================
# Setup Cliente Anthropic
# ==============================================================================
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY or "eyJ" in ANTHROPIC_API_KEY:
    logger.warning("anthropic_key_missing_or_invalid", message="Sua ANTHROPIC_API_KEY parece não estar configurada corretamente.")
    client = None
else:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)


def analyze_workout_chat(chat_text: str, current_rules: dict) -> ChatResponseSchema:
    """
    Usa Claude 3.5 Haiku para interpretar a queixa do usuário e sugerir 
    alterações nas regras de progressão (ex: baixar RPE alvo se estiver com dor).
    Retorna Pydantic validado para garantir a integridade.
    """
    if not client:
        raise ValueError("Anthropic API key is not configured.")

    prompt = f"""
    Você é um especialista em biomecânica e fisiologia do exercício trabalhando como motor auxiliar.
    O usuário disse o seguinte sobre o treino de hoje: "{chat_text}"
    As regras de progressão atuais dele para os exercícios de hoje são:
    {json.dumps(current_rules)}

    Sua tarefa é analisar o relato e ajustar os parâmetros se necessário (ex: diminuir RPE se houver dor).
    Retorne estritamente um JSON com a estrutura requerida.
    """

    logger.info("ai_call_started", model="claude-3-5-haiku-latest", task="nlp_chat")

    response = client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=1024,
        temperature=0.0, # Determinístico
        system="Você responde única e exclusivamente com JSON válido.",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        response_text = response.content[0].text
        # Usamos model_validate_json para forçar que o texto venha na estrutura correta
        validated_data = ChatResponseSchema.model_validate_json(response_text)
        logger.info("ai_call_success", task="nlp_chat")
        return validated_data
    except Exception as exc:
        logger.error("ai_json_parsing_failed", error=str(exc), raw_response=response.content[0].text)
        raise ValueError("A IA retornou um formato inválido.")


def _get_image_base64_from_url(url: str) -> str:
    """Utilitário para baixar a imagem da Signed URL e converter para Base64"""
    response = httpx.get(url)
    response.raise_for_status()
    return base64.b64encode(response.content).decode("utf-8")


def analyze_physique_photo(image_url: str, mime_type: str = "image/jpeg") -> PhysiqueAnalysisSchema:
    """
    Usa Claude 3.5 Sonnet para analisar o físico do usuário a partir de uma Signed URL.
    """
    if not client:
        raise ValueError("Anthropic API key is not configured.")
        
    logger.info("ai_call_started", model="claude-3-5-sonnet-latest", task="vision_analysis")

    try:
        image_base64 = _get_image_base64_from_url(image_url)
    except Exception as exc:
        logger.error("ai_image_download_failed", error=str(exc), url=image_url)
        raise exc

    prompt = """
    Analise esta foto do físico do usuário. 
    Identifique pontos fracos, assimetrias visíveis e faça uma sugestão de ênfase para o próximo bloco de treino.
    Retorne estritamente em JSON.
    """

    response = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=1024,
        temperature=0.2, 
        system="Você é um juiz de fisiculturismo clássico altamente técnico. Responda única e exclusivamente com JSON válido.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
                            "data": image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )

    try:
        response_text = response.content[0].text
        validated_data = PhysiqueAnalysisSchema.model_validate_json(response_text)
        logger.info("ai_call_success", task="vision_analysis")
        return validated_data
    except Exception as exc:
        logger.error("ai_vision_parsing_failed", error=str(exc), raw_response=response.content[0].text)
        raise ValueError("A IA Vision retornou um formato inválido.")
