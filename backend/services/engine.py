from typing import List, Dict, Optional
import structlog

logger = structlog.get_logger()

# ==============================================================================
# Motor de Sobrecarga Progressiva
# ==============================================================================
def calculate_next_weight(current_weight: float, sets: List[dict], rule: dict) -> float:
    """
    Motor determinístico de progressão de carga (Regras + Heurísticas).
    Avalia a performance da última sessão contra as regras de progressão do usuário.
    """
    if not sets:
        return current_weight
    
    # 1. Verifica se todas as séries foram completadas com sucesso
    all_completed = all(s.get("completed", False) for s in sets)
    if not all_completed:
        # Falhou na execução -> Reduz a carga
        decrement = float(rule.get("decrement_percentage", 5.0))
        new_weight = round(current_weight * (1 - decrement / 100), 2)
        logger.info("engine_progression", action="decrement", reason="failed_sets", old_weight=current_weight, new_weight=new_weight)
        return new_weight
    
    # 2. Avalia RPE (se disponível)
    rpes = [s.get("rpe") for s in sets if s.get("rpe") is not None]
    if not rpes:
        # Completou tudo mas sem RPE -> Incremento padrão
        increment = float(rule.get("increment_percentage", 2.5))
        new_weight = round(current_weight * (1 + increment / 100), 2)
        logger.info("engine_progression", action="increment", reason="completed_no_rpe", old_weight=current_weight, new_weight=new_weight)
        return new_weight
        
    avg_rpe = sum(rpes) / len(rpes)
    target_rpe_min = float(rule.get("target_rpe_min", 7.0))
    target_rpe_max = float(rule.get("target_rpe_max", 8.0))
    increment_perc = float(rule.get("increment_percentage", 2.5))
    
    # 3. RPE muito abaixo do alvo -> Esforço baixo demais, duplo incremento
    if avg_rpe < target_rpe_min - 1.0:
        new_weight = round(current_weight * (1 + (increment_perc * 2) / 100), 2)
        logger.info("engine_progression", action="double_increment", reason="rpe_very_low", avg_rpe=avg_rpe, old_weight=current_weight, new_weight=new_weight)
        return new_weight
    
    # 4. RPE dentro ou levemente abaixo do alvo -> Incremento padrão
    if avg_rpe <= target_rpe_max:
        new_weight = round(current_weight * (1 + increment_perc / 100), 2)
        logger.info("engine_progression", action="increment", reason="rpe_in_target", avg_rpe=avg_rpe, old_weight=current_weight, new_weight=new_weight)
        return new_weight
    
    # 5. RPE acima do alvo -> Manter carga
    logger.info("engine_progression", action="maintain", reason="rpe_above_target", avg_rpe=avg_rpe, old_weight=current_weight, new_weight=current_weight)
    return current_weight

# ==============================================================================
# Cálculo de Macros / Calorias (Mifflin-St Jeor)
# ==============================================================================
def calculate_macros(weight_kg: float, height_cm: float, age_years: int, is_male: bool, activity_factor: float, goal: str) -> Dict[str, float]:
    """
    Calcula calorias diárias e divisão de macros usando Mifflin-St Jeor.
    goal: 'cut', 'maintain', 'bulk'
    """
    # Basal Metabolic Rate
    if is_male:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age_years) - 161
        
    tdee = bmr * activity_factor
    
    # Ajuste por objetivo
    if goal == "cut":
        target_calories = tdee - 500
    elif goal == "bulk":
        target_calories = tdee + 300
    else:
        target_calories = tdee
        
    # Distribuição padrão de macros (Alta proteína)
    protein_g = weight_kg * 2.2 # ~2.2g por kg
    fat_g = weight_kg * 1.0     # ~1g por kg
    
    # Restante em carboidratos
    calories_from_protein_fat = (protein_g * 4) + (fat_g * 9)
    carbs_g = (target_calories - calories_from_protein_fat) / 4
    
    # Garante que carbs não fique negativo em cortes muito extremos
    if carbs_g < 0:
        carbs_g = 0
        target_calories = calories_from_protein_fat
        
    logger.info("engine_macros", bmr=bmr, tdee=tdee, target_calories=target_calories, goal=goal)
    
    return {
        "calories": round(target_calories),
        "protein_g": round(protein_g, 1),
        "fat_g": round(fat_g, 1),
        "carbs_g": round(carbs_g, 1)
    }
