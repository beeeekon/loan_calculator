from datetime import date
from app.schemas.dto import LoanStatementRequestDto

def prescoring(dto: LoanStatementRequestDto) -> bool:
    '''проверка заёмщика'''
    today = date.today()
    result: bool = True
    # дата рождения не может быть в будущем
    if dto.birthdate > today:
        result = False
    
    # возраст на сегодня должен быть >= 18 лет
    age = today.year - dto.birthdate.year
    if (today.month, today.day) < (dto.birthdate.month, dto.birthdate.day):
        age -= 1
    if age < 18:
        result = False
    
    # возраст на момент окончания кредита не должен превышать 65 лет
    # считаем, сколько лет пройдет, пока кредит не будет выплачен
    years_to_pay = dto.term // 12
    if dto.term % 12 > 0:
        years_to_pay += 1
        
    age_at_end = age + years_to_pay
    if age_at_end > 65:
        result = False
    
    return result