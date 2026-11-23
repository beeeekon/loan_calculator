from uuid import UUID
from decimal import Decimal
from app.schemas.dto import LoanOfferDto
from app.core.config import settings
from app.services.math_utils import calculate_annuity

def calculate_offers(amount: Decimal, term: int, statement_id: UUID) -> list[LoanOfferDto]:
    ''' перебирает 4 кредитных предложения '''
    offers = []
    
    # Перебираем все 4 комбинации (False/False, False/True, True/False, True/True)
    for insurance in (False, True):
        for salary in (False, True):
            
            #считаем ставку
            rate = settings.BASE_RATE
            if insurance:
                rate -= settings.INSURANCE_DISCOUNT
            if salary:
                rate -= settings.SALARY_DISCOUNT
                
            # считаем итоговую сумму
            total_amount = amount
            if insurance:
                total_amount += amount * settings.INSURANCE_COST_RATE
                
            payment = calculate_annuity(total_amount, rate, term)
            
            offer = LoanOfferDto(
                statementId=statement_id,
                requestedAmount=amount,
                totalAmount=total_amount,
                term=term,
                monthlyPayment=payment,
                rate=rate,
                isInsuranceEnabled=insurance,
                isSalaryClient=salary
            )
            offers.append(offer)
            
    # 5. Сортируем от худшей ставки к лучшей (по убыванию ставки)
    offers.sort(key=lambda x: x.rate, reverse=True) # возьми объект х и верни его поле rate
    
    return offers