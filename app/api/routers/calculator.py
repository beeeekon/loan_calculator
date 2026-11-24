import logging
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from app.schemas.dto import LoanStatementRequestDto, LoanOfferDto, ScoringDataDto, CreditDto
from app.services.prescoring import prescoring
from app.services.offers_calculator import calculate_offers
from app.services.credit_calculator import calculate_credit
from app.core.config import settings


logger = logging.getLogger(__name__)

#префикс /calculator будет у всех эндпоинтов внутри
router = APIRouter(prefix="/calculator", tags=["Calculator"])

@router.post("/offers", response_model=list[LoanOfferDto])
def get_offers(request: LoanStatementRequestDto):
    '''расчет 4 кредитных предложений'''
    
    logger.info(f"Пришел запрос /offers: сумма={request.amount}, срок={request.term}")

    # НОВОЕ: прескоринг
    if not prescoring(request):
        logger.error(f"Код 400: Не пройден прескоринг /offers: дата рождения={request.birthdate}")
        raise HTTPException(status_code=400, detail="Прескоринг не пройден: проверьте возраст и дату рождения")
        
    
    statement_id = uuid4()
    offers = calculate_offers(
        amount=request.amount,
        term=request.term,
        statement_id=statement_id
    )
    logger.info(f"Сгенерировано {len(offers)} предложений для заявки {statement_id}")
    
    return offers


@router.post("/calc", response_model=CreditDto)
def get_credit_calc(request: ScoringDataDto):
    '''полный расчет кредита с графиком платежей'''
    
    logger.info(f"Пришел запрос /calc: сумма={request.amount}, срок={request.term}, страховка={request.isInsuranceEnabled}")
    
    rate = settings.BASE_RATE
    if request.isInsuranceEnabled:
        rate -= settings.INSURANCE_DISCOUNT
    if request.isSalaryClient:
        rate -= settings.SALARY_DISCOUNT
        
    try:
        credit = calculate_credit(
            amount=request.amount,
            term=request.term,
            rate=rate,
            is_insurance=request.isInsuranceEnabled,
            is_salary=request.isSalaryClient
        )
    except Exception as e:
        logger.error(f"Ошибка при расчете кредита: {e}")
        raise HTTPException(status_code=500, detail="Ошибка расчета кредита")
        
    logger.info(f"Успешно рассчитан кредит. Платеж: {credit.monthlyPayment}")
    
    return credit