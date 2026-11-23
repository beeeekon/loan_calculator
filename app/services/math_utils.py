from decimal import Decimal, ROUND_HALF_UP
from datetime import date, timedelta
from app.schemas.dto import PaymentScheduleElementDto

def calculate_annuity(amount: Decimal, rate: Decimal, term: int) -> Decimal:
    '''формула аннуитета'''
    monthly_rate = rate / Decimal("12") / Decimal("100") #годовую ставку в месячную
    if monthly_rate == 0:
        return (amount / term).quantize(Decimal("0.01")) #.quantize(Decimal("0.01")) округление до сотых

    # P / (1 - (1+P)^-N) перевернула в (P * (1+P)^N) / ((1+P)^N - 1 чтоб не было отрицательной степени для денег   
    factor = (monthly_rate * (1 + monthly_rate) ** term) / ((1 + monthly_rate) ** term - 1)

    #множаем сумму на этот коэффициент и округляем до копеек
    return (amount * factor).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def build_schedule(amount: Decimal, rate: Decimal, term: int) -> list[PaymentScheduleElementDto]:
    '''строит график платежей'''
    monthly_payment = calculate_annuity(amount, rate, term)
    monthly_rate = rate / Decimal("12") / Decimal("100")
    remaining = amount # запоминаем сколько мы еще должны банку
    schedule = []
    start_date = date.today()
    
    for i in range(term):
        interest = (remaining * monthly_rate).quantize(Decimal("0.01")) #сколько из платежа уйдет в проценты
        debt = monthly_payment - interest # сколько на сам долг
        remaining -= debt
        
        item = PaymentScheduleElementDto(
            number=i+1,
            date=start_date + timedelta(days=30 * i), # просто прибавляем 30 дней
            totalPayment=monthly_payment,
            interestPayment=interest,
            debtPayment=debt, #тело долга
            remainingDebt=max(remaining, Decimal("0.00")) #остаток не даем уйти в минус
        )
        schedule.append(item)
    return schedule