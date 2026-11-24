import datetime
from decimal import Decimal
from app.services.math_utils import calculate_annuity, build_schedule
from app.services.credit_calculator import calculate_credit

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

def test_annuity_with_zero_rate():
    '''если ставка 0, платеж = сумма / срок'''
    amount = Decimal("12000")
    rate = Decimal("0")
    term = 12
    result = calculate_annuity(amount, rate, term)
    # 12000 / 12 = 1000.00
    assert result == Decimal("1000.00")

def test_schedule_with_small_amount():
    '''график с маленькой суммой чтобы округлился нормально'''
    amount = Decimal("1000")
    rate = Decimal("10")
    term = 3 
    
    schedule = build_schedule(amount, rate, term)
    
    assert len(schedule) == 3

    #проверяем что проценты с каждым месяцем уменьшаются тк уменьшается остаток
    assert schedule[0].interestPayment > schedule[1].interestPayment
    #проверяем что тело долга с каждым месяцем растет
    assert schedule[0].debtPayment < schedule[1].debtPayment
    #проверяем что в конце остаток 0
    assert schedule[-1].remainingDebt <= Decimal("0.01")

def test_schedule_structure():
    ''' все ли поля графика заполнены правильно'''
    schedule = build_schedule(Decimal("50000"), Decimal("12"), 2)
    
    first = schedule[0]
    assert first.number == 1
    assert isinstance(first.date, datetime.date)
    assert first.totalPayment > 0
    assert first.interestPayment > 0
    assert first.debtPayment > 0
    assert first.remainingDebt > 0

def test_credit_without_insurance():
    '''страховки нет итоговая сумма не меняется'''
    result = calculate_credit(
        amount=Decimal("100000"),
        term=12,
        rate=Decimal("15"),
        is_insurance=False,
        is_salary=False
    )
    
    assert result.amount == Decimal("100000")
    assert result.monthlyPayment > 0
    assert result.psk > 0
    # НОВОЕ: проверяем, что ПСК равна ставке (так как страховки нет)
    assert result.psk == Decimal("15.00")