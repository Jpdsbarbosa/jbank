from dataclasses import dataclass
import re


@dataclass(frozen=True)
class CPF:
    """
    Representa um CPF válido.
    
    Atributos:
        value: CPF sem máscara (apenas números)
    """
    value: str
    
    def __post_init__(self) -> None:
        """Valida o CPF após inicialização."""
        # Limpa o CPF (remove pontos, traços, espaços)
        cleaned = re.sub(r'[.\-\s]', '', self.value)
        
        # Como é frozen, usamos object.__setattr__
        object.__setattr__(self, 'value', cleaned)
        
        if not self._is_valid():
            raise ValueError("Invalid CPF")

    def _is_valid(self) -> bool:
        if len(self.value ) != 11:
            return False

        if not self.value.isdigit():
            return False

        if self.value == self.value[0] * 11:
            return False

        return self._validate_check_digits()

    def _validate_check_digits(self) -> bool:

        sum_first = sum(
            int(self.value[i]) * (10 -i)
            for i in range(9)
        )

        first_digit = (sum_first * 10) % 11
        if first_digit == 10:
            first_digit = 0

        sum_second = sum(
            int(self.value[i]) * (11 -i)
            for i in range(10)
        )

        second_digit = (sum_second * 10) % 11
        if second_digit == 10:
            second_digit = 0
        
        return (
            int(self.value[9]) == first_digit and
            int(self.value[10]) == second_digit
        )

    def formatted(self) -> str:
        return f"{self.value[:3]}.{self.value[3:6]}.{self.value[6:9]}-{self.value[-2:]}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CPF):
            return False
        return self.value == other.value
    
    def __str__(self) -> str:
        return self.formatted()

    def __repr__(self) -> str:
        return f"CPF({self.value})"