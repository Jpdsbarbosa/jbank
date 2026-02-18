from dataclasses import dataclass, field
from decimal import Decimal
from typing import Union


@dataclass(frozen=True)
class Money:
    """Representa valores monetários de forma segura."""
    amount: Decimal
    
    def __post_init__(self) -> None:
        """Valida após inicialização."""
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
    
    @staticmethod
    def create(value: Union[int, float, str, Decimal]) -> 'Money':
        """Factory method para criar Money de vários tipos."""
        return Money(amount=Decimal(str(value)))
    
    def add(self, other: 'Money') -> 'Money':
        return Money(self.amount + other.amount)
    
    def subtract(self, other: 'Money') -> 'Money':
        if self.amount - other.amount < 0:
            raise ValueError("Amount cannot be negative")
        return Money(self.amount - other.amount)
    
    def is_greater_than(self, other: 'Money') -> bool:
        return self.amount > other.amount
    
    def is_greater_or_equal(self, other: 'Money') -> bool:
        return self.amount >= other.amount
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount
    
    def __str__(self) -> str:
        return f"R$ {self.amount:.2f}"
    
    def __repr__(self) -> str:
        return f"Money({self.amount})"