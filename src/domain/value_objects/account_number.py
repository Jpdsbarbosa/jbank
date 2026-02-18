from dataclasses import dataclass
import uuid

@dataclass(frozen=True)
class AccountNumber:
    value: str


    def __post_init__(self) -> None:
        if not self.value.startswith("ACC-"):
            raise ValueError("Account number must start with 'ACC-'")
        
        if len(self.value) != 40:
            raise ValueError("Account number must be 40 characters long")

    
    @staticmethod
    def generate() -> "AccountNumber":
        return AccountNumber(value=f"ACC-{uuid.uuid4()}")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AccountNumber):
            return False
        return self.value == other.value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"AccountNumber({self.value})"   