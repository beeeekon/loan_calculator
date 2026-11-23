from fastapi.testclient import TestClient
from app.main import app

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