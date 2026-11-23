from decimal import Decimal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
       
    #env_file=".env" означает что pydantic будет искать файл .env в корне проекта
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    #базовая процентная ставка
    BASE_RATE: Decimal = Decimal("15.0")
    
    #скидка при оформлении страховки (вычитается из ставки)
    INSURANCE_DISCOUNT: Decimal = Decimal("3.0")
    
    #скидка для зарплатных клиентов (вычитается из ставки)
    SALARY_DISCOUNT: Decimal = Decimal("1.0")
    
    #стоимость страховки (процент от суммы кредита, добавляется в тело кредита)
    INSURANCE_COST_RATE: Decimal = Decimal("0.05")

#создаем экземпляр настроек. Теперь их можно импортировать в другие файлы
settings = Settings()