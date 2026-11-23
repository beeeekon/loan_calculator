from decimal import Decimal
from app.services.math_utils import calculate_annuity, build_schedule

def test_calculate_annuity():
    # 100 000 под 15% на 12 месяцев
    amount = Decimal("100000")
    rate = Decimal("15")
    term = 12
    
    #ожидаемый результат для этих параметров (примерно 9025.83)
    result = calculate_annuity(amount, rate, term)
    
    
    assert result > 0 
    assert isinstance(result, Decimal)
    
    assert result == Decimal("9025.83") #проверяем точное значение до копеек

def test_build_schedule():
    amount = Decimal("100000")
    rate = Decimal("15")
    term = 12
    
    schedule = build_schedule(amount, rate, term)
    
    
    assert len(schedule) == term #проверяем что в графике ровно 12 месяцев
    
    assert schedule[0].number == 1 #проверяем что первый платеж имеет номер 1
    
    assert schedule[-1].remainingDebt <= Decimal("0.01") #проверяем что остаток в конце равен 0 (или очень близок к нулю)