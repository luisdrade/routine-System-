import os
import json
import httpx
import base64
import structlog
from google import genai
from google.genai import types
from dotenv import load_dotenv

from models.schemas import ChatResponseSchema, PhysiqueAnalysisSchema, VirtualAssistantResponse

load_dotenv(override=True)
logger = structlog.get_logger()

# ==============================================================================
# Setup Cliente Google GenAI (Nova SDK)
# ==============================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logger.warning("gemini_key_missing_or_invalid", message="Sua GEMINI_API_KEY parece não estar configurada corretamente.")
    client = None
else:
    client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_workout_chat(chat_text: str, current_rules: dict) -> ChatResponseSchema:
    if not client:
        raise ValueError("Gemini API key is not configured.")

    prompt = f"""
    Você é um especialista em biomecânica e fisiologia do exercício trabalhando como motor auxiliar.
    O usuário disse o seguinte sobre o treino de hoje: "{chat_text}"
    As regras de progressão atuais dele para os exercícios de hoje são:
    {json.dumps(current_rules)}

    Sua tarefa é analisar o relato e ajustar os parâmetros se necessário (ex: diminuir RPE se houver dor).
    Retorne estritamente um JSON com a estrutura requerida.
    """

    logger.info("ai_call_started", model="gemini-2.5-flash", task="nlp_chat")

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.0,
            system_instruction="Você responde única e exclusivamente com JSON válido seguindo o formato de lista de adjustments."
        )
    )

    try:
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        validated_data = ChatResponseSchema.model_validate_json(response_text)
        logger.info("ai_call_success", task="nlp_chat")
        return validated_data
    except Exception as exc:
        logger.error("ai_json_parsing_failed", error=str(exc), raw_response=response.text)
        raise ValueError("A IA retornou um formato inválido.")


def converse_with_assistant(chat_history: list, user_message: str) -> VirtualAssistantResponse:
    if not client:
        raise ValueError("Gemini API key is not configured.")

    system_prompt = """
    Você é o Assistente Virtual Pessoal de Treino e Nutrição do usuário.
    Seja extremamente conciso, direto e natural. Aja como um humano prestativo.
    Seu objetivo principal é descobrir (sem parecer um formulário robótico) as seguintes métricas:
    - Peso Atual (kg)
    - Objetivo (cut, bulk ou maintain)
    - Nível de atividade diária
    - Dores ou lesões
    
    Você OBRIGATORIAMENTE deve retornar APENAS um JSON com os seguintes campos:
    - "reply_message": string com a sua fala para o usuário
    - "extracted_data": um objeto com "current_weight_kg", "current_goal", "activity_factor", e "reported_pains"
    - "requires_more_info": boolean indicando se ainda precisa fazer perguntas.
    """

    # Gemini history format
    formatted_history = []
    for msg in chat_history:
        role = "model" if msg["role"] == "assistant" else "user"
        formatted_history.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))
        
    # Append the new user message
    formatted_history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_message)]))

    logger.info("ai_call_started", model="gemini-2.5-flash", task="conversational_agent")

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=formatted_history,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.4,
            system_instruction=system_prompt
        )
    )

    try:
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        validated_data = VirtualAssistantResponse.model_validate_json(response_text)
        logger.info("ai_call_success", task="conversational_agent", extracted_data=validated_data.extracted_data.model_dump())
        return validated_data
    except Exception as exc:
        logger.error("ai_json_parsing_failed", error=str(exc), raw_response=response.text)
        raise ValueError(f"A IA retornou um formato inválido: {response_text}")


def _get_image_base64_from_url(url: str) -> str:
    response = httpx.get(url)
    response.raise_for_status()
    return base64.b64encode(response.content).decode("utf-8")


def analyze_physique_photo(image_url: str, mime_type: str = "image/jpeg") -> PhysiqueAnalysisSchema:
    if not client:
        raise ValueError("Gemini API key is not configured.")
        
    logger.info("ai_call_started", model="gemini-2.5-pro", task="vision_analysis")

    try:
        response_img = httpx.get(image_url)
        response_img.raise_for_status()
    except Exception as exc:
        logger.error("ai_image_download_failed", error=str(exc), url=image_url)
        raise exc

    prompt = """
    Analise esta foto do físico do usuário. 
    Identifique pontos fracos, assimetrias visíveis e faça uma sugestão de ênfase para o próximo bloco de treino.
    Retorne estritamente em JSON com "weak_points" (lista), "asymmetries" (lista), "emphasis_suggestion" (string) e "recommended_exercise_adjustments" (lista).
    """

    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=[
            prompt,
            types.Part.from_bytes(data=response_img.content, mime_type=mime_type)
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2,
            system_instruction="Você é um juiz de fisiculturismo clássico altamente técnico. Responda única e exclusivamente com JSON válido."
        )
    )

    try:
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()

        validated_data = PhysiqueAnalysisSchema.model_validate_json(response_text)
        logger.info("ai_call_success", task="vision_analysis")
        return validated_data
    except Exception as exc:
        logger.error("ai_vision_parsing_failed", error=str(exc), raw_response=response.text)
        raise ValueError("A IA Vision retornou um formato inválido.")
