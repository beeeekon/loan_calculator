from decimal import Decimal
from uuid import UUID
import datetime
from pydantic import BaseModel, Field


class LoanStatementRequestDto(BaseModel):
    '''Запрос на расчёт предложений'''
    amount: Decimal = Field(gt=0, description="Сумма кредита") #gt - строго больше
    term: int = Field(gt=0, le=60, description="Срок в месяцах") #le - меньше или равно
    firstName: str = Field(min_length=2, max_length=50, description="Имя")
    lastName: str = Field(min_length=2, max_length=50, description="Фамилия")
    middleName: str = Field(min_length=2, max_length=50, description="Отчество")
    email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$", description="Электронная почта") # проверка на email из дипсика
    birthdate: datetime.date = Field(description="Дата рождения")
    passportSeries: str = Field(pattern=r"^\d{4}$", description="Серия паспорта (4 цифры)") # ^ начало строки \d{} строго столько 
    passportNumber: str = Field(pattern=r"^\d{6}$", description="Номер паспорта (6 цифр)")# $ конец строки

class LoanOfferDto(BaseModel):
    '''Кредитное предложение (возвращается списком)'''
    statementId: UUID = Field(description="ID заявки")
    requestedAmount: Decimal = Field(description="Запрашиваемая сумма")
    totalAmount: Decimal = Field(description="Итоговая сумма (с учетом страховки)")
    term: int = Field(description="Срок в месяцах")
    monthlyPayment: Decimal = Field(description="Ежемесячный платеж")
    rate: Decimal = Field(description="Процентная ставка")
    isInsuranceEnabled: bool = Field(description="Включена ли страховка")
    isSalaryClient: bool = Field(description="Является ли зарплатным клиентом")


class ScoringDataDto(BaseModel):
    '''Данные для полного расчета кредита'''
    amount: Decimal = Field(gt=0, description="Сумма кредита")
    term: int = Field(gt=0, le=60, description="Срок в месяцах")
    firstName: str = Field(description="Имя")
    lastName: str = Field(description="Фамилия")
    middleName: str = Field(description="Отчество")
    birthdate: datetime.date = Field(description="Дата рождения")
    passportSeries: str = Field(description="Серия паспорта")
    passportNumber: str = Field(description="Номер паспорта")
    isInsuranceEnabled: bool = Field(description="Включена ли страховка")
    isSalaryClient: bool = Field(description="Является ли зарплатным клиентом")


class PaymentScheduleElementDto(BaseModel):
    '''Элемент графика платежей'''
    number: int = Field(description="Порядковый номер платежа")
    date: datetime.date = Field(description="Дата платежа")
    totalPayment: Decimal = Field(description="Общая сумма платежа")
    interestPayment: Decimal = Field(description="Сумма процентов")
    debtPayment: Decimal = Field(description="Сумма основного долга")
    remainingDebt: Decimal = Field(description="Остаток долга")

class CreditDto(BaseModel):
    '''Итоговый ответ по кредиту'''
    amount: Decimal = Field(description="Сумма кредита")
    term: int = Field(description="Срок в месяцах")
    monthlyPayment: Decimal = Field(description="Ежемесячный платеж")
    rate: Decimal = Field(description="Ставка")
    psk: Decimal = Field(description="Полная стоимость кредита")
    isInsuranceEnabled: bool = Field(description="Страховка")
    isSalaryClient: bool = Field(description="Зарплатный клиент")
    #от "худшего" к "лучшему" (чем меньше итоговая ставка, тем лучше).
    paymentSchedule: list[PaymentScheduleElementDto] = Field(description="График платежей")