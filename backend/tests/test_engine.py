import pytest
from services.engine import calculate_next_weight, calculate_macros

@pytest.fixture
def default_rule():
    return {
        "target_rpe_min": 7.0,
        "target_rpe_max": 8.0,
        "increment_percentage": 2.5,
        "decrement_percentage": 5.0
    }

def test_engine_decrements_weight_on_failed_set(default_rule):
    current_weight = 100.0
    sets = [
        {"completed": True, "rpe": 8},
        {"completed": False, "rpe": 10} # falhou
    ]
    # Esperado: 100 - 5% = 95.0
    next_weight = calculate_next_weight(current_weight, sets, default_rule)
    assert next_weight == 95.0

def test_engine_increments_weight_no_rpe(default_rule):
    current_weight = 100.0
    sets = [
        {"completed": True},
        {"completed": True}
    ]
    # Esperado: 100 + 2.5% = 102.5
    next_weight = calculate_next_weight(current_weight, sets, default_rule)
    assert next_weight == 102.5

def test_engine_double_increments_when_rpe_is_very_low(default_rule):
    current_weight = 100.0
    sets = [
        {"completed": True, "rpe": 5.0},
        {"completed": True, "rpe": 5.5}
    ]
    # avg = 5.25. Muito menor que 7.0 - 1.0 (6.0)
    # Esperado: 100 + 5.0% = 105.0
    next_weight = calculate_next_weight(current_weight, sets, default_rule)
    assert next_weight == 105.0

def test_engine_increments_normally_in_target_rpe(default_rule):
    current_weight = 100.0
    sets = [
        {"completed": True, "rpe": 7.5},
        {"completed": True, "rpe": 8.0}
    ]
    # avg = 7.75. Entre 7.0 e 8.0
    # Esperado: 100 + 2.5% = 102.5
    next_weight = calculate_next_weight(current_weight, sets, default_rule)
    assert next_weight == 102.5

def test_engine_maintains_weight_above_target_rpe(default_rule):
    current_weight = 100.0
    sets = [
        {"completed": True, "rpe": 9.0},
        {"completed": True, "rpe": 9.5}
    ]
    # avg = 9.25. Acima de 8.0.
    # Esperado: 100.0 (mantém)
    next_weight = calculate_next_weight(current_weight, sets, default_rule)
    assert next_weight == 100.0

def test_calculate_macros_cut():
    # Homem de 80kg, 180cm, 30 anos, ativo leve (1.375) fazendo cut.
    # BMR = (10*80) + (6.25*180) - (5*30) + 5 = 800 + 1125 - 150 + 5 = 1780
    # TDEE = 1780 * 1.375 = ~2447.5
    # Target cut = ~1947.5
    macros = calculate_macros(80, 180, 30, True, 1.375, "cut")
    
    assert macros["calories"] == 1948
    assert macros["protein_g"] == 176.0 # 80 * 2.2
    assert macros["fat_g"] == 80.0    # 80 * 1
    # carbs = (1948 - (176*4) - (80*9)) / 4 = (1948 - 704 - 720)/4 = 524/4 = 131
    assert macros["carbs_g"] == 130.9 # math rounding diffs are fine
