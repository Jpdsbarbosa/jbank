# 🏦 JBank - Sistema Bancário Educacional

Sistema bancário simplificado construído com **Clean Architecture + DDD** para aprendizado de Python moderno, mensageria e NoSQL.

## 🎯 Objetivo

Projeto educacional para praticar:
- ✅ Python moderno com type hints
- ✅ Clean Architecture + Domain-Driven Design
- ✅ FastAPI (API REST)
- ✅ MongoDB (NoSQL)
- ✅ RabbitMQ (Mensageria/Filas)
- ✅ Docker & Docker Compose

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│         (FastAPI - API REST)            │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│        Application Layer                │
│     (Use Cases - Regras de Aplicação)   │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│          Domain Layer                   │
│  (Entidades, Value Objects, Eventos)    │
│         ❤️ NÚCLEO DO SISTEMA            │
└──────────────▲──────────────────────────┘
               │
┌──────────────┴──────────────────────────┐
│       Infrastructure Layer              │
│   (MongoDB, RabbitMQ, Repositórios)     │
└─────────────────────────────────────────┘
```

### 📂 Estrutura de Pastas

```
src/
├── domain/              # Coração - Lógica de negócio pura
│   ├── entities/        # Account, Transaction
│   ├── value_objects/   # Money, AccountNumber, CPF
│   ├── events/          # Eventos de domínio
│   └── repositories/    # Interfaces (abstrações)
├── application/         # Casos de uso
│   ├── use_cases/       # CreateAccount, Transfer, Deposit
│   └── services/        # Serviços de aplicação
├── infrastructure/      # Implementações técnicas
│   ├── database/        # MongoDB repositories
│   ├── messaging/       # RabbitMQ producers/consumers
│   └── config/          # Configurações
└── presentation/        # API REST
    ├── api/             # Rotas FastAPI
    └── schemas/         # Pydantic models (DTOs)
```

## 🚀 Como Rodar

### Pré-requisitos
- Docker & Docker Compose
- Python 3.11+

### Iniciar os serviços

```bash
# Subir MongoDB e RabbitMQ
docker-compose up -d

# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
python -m uvicorn src.presentation.main:app --reload
```

### Acessar

- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)

## 📚 Funcionalidades

### Operações Síncronas (Imediatas)
- ✅ Criar conta bancária
- ✅ Consultar saldo
- ✅ Consultar extrato
- ✅ Depositar dinheiro

### Operações Assíncronas (Via Fila)
- 🔄 Transferências entre contas
  - A transferência vai para uma fila
  - Um worker processa de forma assíncrona
  - Eventos são emitidos quando completa

## 🧠 Conceitos Principais

### DDD (Domain-Driven Design)
- **Entidades**: Objetos com identidade única (Account)
- **Value Objects**: Objetos sem identidade, definidos por valores (Money, CPF)
- **Agregados**: Conjunto de entidades tratadas como uma unidade
- **Eventos de Domínio**: Algo importante que aconteceu (TransferCompleted)
- **Repositórios**: Abstrações para persistência

### Clean Architecture
- **Dependência para dentro**: Camadas externas dependem das internas
- **Domain não conhece nada**: É completamente isolado
- **Inversão de dependência**: Usamos interfaces/abstrações

### Mensageria (RabbitMQ)
- **Producer**: Envia mensagens para a fila
- **Consumer**: Processa mensagens da fila
- **Queue**: Fila que armazena mensagens
- **Exchange**: Roteador de mensagens

## 📖 Aprendizados

Este projeto te ensina:
1. **Python Moderno**: Type hints, dataclasses, async/await
2. **NoSQL (MongoDB)**: Documentos, queries, indexes
3. **Mensageria**: Filas, producers, consumers, eventos
4. **Arquitetura**: Separação de responsabilidades, testabilidade
5. **FastAPI**: API REST moderna e rápida

## 🧪 Testes

```bash
# Rodar todos os testes
pytest

# Com coverage
pytest --cov=src tests/
```

## 📝 Exemplos de Uso

### Criar uma conta

```bash
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "holder_name": "João Paulo",
    "cpf": "12345678900",
    "initial_balance": 1000.00
  }'
```

### Fazer uma transferência

```bash
curl -X POST http://localhost:8000/api/transfers \
  -H "Content-Type: application/json" \
  -d '{
    "from_account": "ACC-001",
    "to_account": "ACC-002",
    "amount": 150.00
  }'
```

## 🎓 Próximos Passos

Após dominar este projeto, você pode adicionar:
- [ ] Autenticação JWT
- [ ] Rate limiting
- [ ] Logs estruturados
- [ ] Métricas e observabilidade
- [ ] Saga pattern para transações distribuídas
- [ ] Event Sourcing
- [ ] CQRS (Command Query Responsibility Segregation)

---

**Desenvolvido para aprendizado antes de entrar no Stark Banking! 🚀**
