from decimal import Decimal

from fastapi.testclient import TestClient
from app.main import app

#ЧТОБЫ ЗАПУСТИТЬ ТЕСТЫ python -m pytest

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_get_offers():
    payload = {
        "amount": 100000,
        "term": 12,
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "middleName": "Ivanovich",
        "email": "ivan@test.com",
        "birthdate": "1990-01-01",
        "passportSeries": "1234",
        "passportNumber": "123456"
    }
    response = client.post("/calculator/offers", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 4 #должно вернуться 4 предложения
    
    assert "rate" in data[0]  #проверяем что в ответе есть нужные поля
    assert "monthlyPayment" in data[0]

def test_get_calc():
    payload = {
        "amount": 100000,
        "term": 12,
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "middleName": "Ivanovich",
        "birthdate": "1990-01-01",
        "passportSeries": "1234",
        "passportNumber": "123456",
        "isInsuranceEnabled": True,
        "isSalaryClient": False
    }
    response = client.post("/calculator/calc", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    #проверяем наличие графика платежей
    assert "paymentSchedule" in data
    assert len(data["paymentSchedule"]) == 12

#///////////////////ВАЛИДЦИЯ//////

def test_offers_invalid_amount():
    '''при отрицательной сумме вернется 422?'''
    payload = {
        "amount": -100,
        "term": 12,
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "middleName": "Ivanovich",
        "email": "ivan@test.com",
        "birthdate": "1990-01-01",
        "passportSeries": "1234",
        "passportNumber": "123456"
    }
    response = client.post("/calculator/offers", json=payload)
    
    assert response.status_code == 422
    #проверяем что ошибка связана именно с суммой
    assert "amount" in response.text

def test_offers_invalid_email():
    '''кривой email'''
    payload = {
        "amount": 100000,
        "term": 12,
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "middleName": "Ivanovich",
        "email": "ivan_no_at", # Нет собачки
        "birthdate": "1990-01-01",
        "passportSeries": "1234",
        "passportNumber": "123456"
    }
    response = client.post("/calculator/offers", json=payload)
    assert response.status_code == 422
    assert "email" in response.text

def test_offers_invalid_term():
    '''срок больше 60'''
    payload = {
        "amount": 100000,
        "term": 120, # Больше лимита
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "middleName": "Ivanovich",
        "email": "ivan@test.com",
        "birthdate": "1990-01-01",
        "passportSeries": "1234",
        "passportNumber": "123456"
    }
    response = client.post("/calculator/offers", json=payload)
    assert response.status_code == 422
    assert "term" in response.text

def test_offers_invalid_passport_series():
    '''серия паспорта с буквами'''
    payload = {
        "amount": 100000,
        "term": 12,
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "middleName": "Ivanovich",
        "email": "ivan@test.com",
        "birthdate": "1990-01-01",
        "passportSeries": "12AB",
        "passportNumber": "123456"
    }
    response = client.post("/calculator/offers", json=payload)
    

    assert response.status_code == 422
    #проверяем что ошибка связана именно с passportSeries
    assert "passportSeries" in response.text

#///////////////////ЛОГИКА//////
def test_offers_structure_and_sorting():
    '''проверяем что предложения отсортированы от худшего к лучшему и имеют все поля'''
    payload = {
        "amount": 100000,
        "term": 12,
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "middleName": "Ivanovich",
        "email": "ivan@test.com",
        "birthdate": "1990-01-01",
        "passportSeries": "1234",
        "passportNumber": "123456"
    }
    response = client.post("/calculator/offers", json=payload)
    data = response.json()
    
    #роверяем что ставки идут по убыванию
    rates = [offer["rate"] for offer in data]
    assert rates == sorted(rates, reverse=True)
    
    # все ли поля на месте
    first_offer = data[0]
    assert "statementId" in first_offer
    assert "requestedAmount" in first_offer
    assert "totalAmount" in first_offer
    assert "monthlyPayment" in first_offer
    assert "isInsuranceEnabled" in first_offer
    assert "isSalaryClient" in first_offer


def test_calc_with_insurance():
    '''страховка должна влиять на итоговую сумму и график'''
    payload = {
        "amount": 100000,
        "term": 12,
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "middleName": "Ivanovich",
        "birthdate": "1990-01-01",
        "passportSeries": "1234",
        "passportNumber": "123456",
        "isInsuranceEnabled": True,  # Включаем страховку
        "isSalaryClient": False
    }
    response = client.post("/calculator/calc", json=payload)
    data = response.json()
    
    #итоговая сумма должна быть больше изначальной 100000 + 5%
    assert Decimal(data["amount"]) > Decimal("100000")
    assert data["isInsuranceEnabled"] is True
    #проверяем пск
    assert Decimal(data["psk"]) > Decimal("0")