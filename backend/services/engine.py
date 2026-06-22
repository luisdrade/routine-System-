from typing import List

def calculate_next_weight(current_weight: float, sets: List[dict], rule: dict) -> float:
    """
    Motor determinístico de progressão de carga (Substituindo o antigo kNN).
    Avalia a performance da última sessão contra as regras de progressão do usuário.
    """
    if not sets:
        return current_weight
    
    # 1. Verifica se todas as séries foram completadas com sucesso
    all_completed = all(s.get("completed", False) for s in sets)
    if not all_completed:
        # Falhou na execução -> Reduz a carga
        decrement = rule.get("decrement_percentage", 5.0)
        return round(current_weight * (1 - decrement / 100), 2)
    
    # 2. Avalia RPE (se disponível)
    rpes = [s.get("rpe") for s in sets if s.get("rpe") is not None]
    if not rpes:
        # Completou tudo mas sem RPE -> Incremento padrão
        increment = rule.get("increment_percentage", 2.5)
        return round(current_weight * (1 + increment / 100), 2)
        
    avg_rpe = sum(rpes) / len(rpes)
    
    # 3. Regra de RPE dentro/abaixo do alvo -> Incrementa
    if avg_rpe <= rule.get("target_rpe_max", 8.0):
        increment = rule.get("increment_percentage", 2.5)
        return round(current_weight * (1 + increment / 100), 2)
    
    # 4. RPE acima do alvo -> Mantém a carga
    return current_weight
