from pydantic import BaseModel, Field
from typing import List, Optional

# ==============================================================================
# Modelos para IA Conversacional (Ajuste de Treino)
# ==============================================================================
class WorkoutAdjustment(BaseModel):
    exercise_id: str
    target_rpe_adjustment: float = Field(default=0.0, description="Mudança no alvo de RPE, ex: -1.0 para diminuir intensidade")
    increment_percentage_adjustment: float = Field(default=0.0, description="Mudança no % de incremento")
    reasoning: str = Field(description="A justificativa da IA baseada na reclamação/texto do usuário")

class ChatResponseSchema(BaseModel):
    adjustments: List[WorkoutAdjustment] = Field(description="Lista de ajustes recomendados para a sessão atual ou regras gerais")

# ==============================================================================
# Modelos para IA Conversacional Dinâmica (Atendente Virtual)
# ==============================================================================
class ExtractedMetrics(BaseModel):
    current_weight_kg: Optional[float] = Field(default=None, description="Peso extraído do chat, se mencionado")
    current_goal: Optional[str] = Field(default=None, description="Objetivo extraído (cut, bulk, maintain)")
    activity_factor: Optional[float] = Field(default=None, description="Fator de atividade estimado baseado no relato (ex: 1.2 sedentário, 1.55 moderado)")
    reported_pains: Optional[List[str]] = Field(default=[], description="Dores ou lesões relatadas")

class VirtualAssistantResponse(BaseModel):
    reply_message: str = Field(description="A mensagem natural que o assistente responderá ao usuário no chat")
    extracted_data: ExtractedMetrics = Field(description="Dados estruturados extraídos secretamente a partir da conversa")
    requires_more_info: bool = Field(default=False, description="True se o assistente precisar fazer mais perguntas para finalizar o onboarding")


# ==============================================================================
# Modelos para IA Visual (Análise de Físico)
# ==============================================================================
class PhysiqueAnalysisSchema(BaseModel):
    weak_points: List[str] = Field(description="Lista de pontos fracos identificados (ex: 'Posterior de ombro', 'Panturrilha')")
    asymmetries: List[str] = Field(description="Assimetrias visíveis (ex: 'Braço esquerdo levemente menor')")
    emphasis_suggestion: str = Field(description="Sugestão em linguagem natural do que focar nos próximos treinos")
    recommended_exercise_adjustments: List[str] = Field(description="Sugestões de alterações ou inclusões de exercícios")
