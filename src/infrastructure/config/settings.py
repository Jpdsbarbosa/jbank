from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    configurações da aplicação carregadas pelo .env

    O PyDantic valida automaticamente os tipos e
    pode definir valores padrão
    """

    # Application
    app_name: str = "JBank"
    app_version: str = "1.0.0"
    environment: str = "development"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # MongoDB
    mongodb_url: str = "mongodb://admin:admin123@localhost:27017"
    mongodb_database: str = "jbank"

    # RabbitMQ
    rabbitmq_url: str = "amqp://admin:admin123@localhost:5672/"
    rabbitmq_exchange: str = "jbank_events"
    rabbitmq_transfer_queue: str = "jbank_transfer_queue"

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=False,
    ) 


settings = Settings()