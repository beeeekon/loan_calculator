from decimal import Decimal
from app.schemas.dto import CreditDto
from app.core.config import settings
from app.services.math_utils import calculate_annuity, build_schedule

def calculate_credit(amount: Decimal, term: int, rate: Decimal, is_insurance: bool, is_salary: bool) -> CreditDto:
    '''cобирает полный расчет кредита '''
    
    #cчитаем сумму с учетом страховки
    final_amount = amount
    if is_insurance:
        final_amount += amount * settings.INSURANCE_COST_RATE
        
    payment = calculate_annuity(final_amount, rate, term)
    schedule = build_schedule(final_amount, rate, term)
    
    # cчитаем ПСК полная стоимость кредита
    total_paid = payment * term
    psk = ((total_paid / final_amount) * Decimal("100") - Decimal("100")).quantize(Decimal("0.01"))
    
    # 4. Создаем и возвращаем итоговый DTO
    result = CreditDto(
        amount=final_amount,
        term=term,
        monthlyPayment=payment,
        rate=rate,
        psk=psk,
        isInsuranceEnabled=is_insurance,
        isSalaryClient=is_salary,
        paymentSchedule=schedule
    )
    
    return result