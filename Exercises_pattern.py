from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional, Type
import json


# Exercise 1

class PaymentProcessor(ABC):
    @abstractmethod
    def validate(self, details: dict) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def process(self, amount: float, details: dict) -> dict:
        raise NotImplementedError


class CreditCardProcessor(PaymentProcessor):
    def validate(self, details: dict) -> Optional[str]:
        card_number = details.get("card_number")
        cvv = details.get("cvv")
        if not card_number or len(str(card_number)) != 16:
            return "Invalid card number"
        if not cvv or len(str(cvv)) != 3:
            return "Invalid CVV"
        return None

    def process(self, amount: float, details: dict) -> dict:
        error = self.validate(details)
        if error:
            return {"success": False, "error": error}
        fee = amount * 0.029
        return {"success": True, "method": "credit_card", "amount": amount + fee, "fee": fee}


class BankTransferProcessor(PaymentProcessor):
    def validate(self, details: dict) -> Optional[str]:
        iban = details.get("iban")
        if not iban or len(str(iban)) < 15:
            return "Invalid IBAN"
        return None

    def process(self, amount: float, details: dict) -> dict:
        error = self.validate(details)
        if error:
            return {"success": False, "error": error}
        fee = 1.50
        return {"success": True, "method": "bank_transfer", "amount": amount + fee, "fee": fee}


class PayPalProcessor(PaymentProcessor):
    def validate(self, details: dict) -> Optional[str]:
        email = details.get("email")
        if not email or "@" not in str(email):
            return "Invalid PayPal email"
        return None

    def process(self, amount: float, details: dict) -> dict:
        error = self.validate(details)
        if error:
            return {"success": False, "error": error}
        fee = amount * 0.034 + 0.30
        return {"success": True, "method": "paypal", "amount": amount + fee, "fee": fee}


class PaymentFactory:
    def __init__(self) -> None:
        self._registry: Dict[str, Type[PaymentProcessor]] = {
            "credit_card": CreditCardProcessor,
            "bank_transfer": BankTransferProcessor,
            "paypal": PayPalProcessor,
        }

    def register(self, payment_type: str, processor_cls: Type[PaymentProcessor]) -> None:
        self._registry[payment_type] = processor_cls

    def get_processor(self, payment_type: str) -> PaymentProcessor:
        cls = self._registry.get(payment_type)
        if not cls:
            raise ValueError(f"Unknown payment type: {payment_type}")
        return cls()


# Exercise 2: Builder Pattern

@dataclass(frozen=True)
class Employee:
    first_name: str
    last_name: str
    email: str
    department: str
    position: str
    salary: float
    start_date: str
    manager_id: Optional[int] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    has_parking: bool = False
    has_laptop: bool = False
    has_vpn_access: bool = False
    has_admin_rights: bool = False
    office_location: Optional[str] = None
    contract_type: str = "permanent"


class EmployeeBuilder:
    def __init__(self) -> None:
        self._d: Dict[str, Any] = {
            "manager_id": None,
            "phone": None,
            "address": None,
            "emergency_contact": None,
            "has_parking": False,
            "has_laptop": False,
            "has_vpn_access": False,
            "has_admin_rights": False,
            "office_location": None,
            "contract_type": "permanent",
        }

    def with_name(self, first_name: str, last_name: str) -> "EmployeeBuilder":
        self._d["first_name"] = first_name
        self._d["last_name"] = last_name
        return self

    def with_email(self, email: str) -> "EmployeeBuilder":
        self._d["email"] = email
        return self

    def with_job(self, department: str, position: str, salary: float, start_date: str) -> "EmployeeBuilder":
        self._d["department"] = department
        self._d["position"] = position
        self._d["salary"] = salary
        self._d["start_date"] = start_date
        return self

    def with_contact(self, phone: Optional[str] = None, address: Optional[str] = None,
                     emergency_contact: Optional[str] = None) -> "EmployeeBuilder":
        if phone is not None:
            self._d["phone"] = phone
        if address is not None:
            self._d["address"] = address
        if emergency_contact is not None:
            self._d["emergency_contact"] = emergency_contact
        return self

    def with_equipment(self, laptop: Optional[bool] = None, parking: Optional[bool] = None) -> "EmployeeBuilder":
        if laptop is not None:
            self._d["has_laptop"] = laptop
        if parking is not None:
            self._d["has_parking"] = parking
        return self

    def with_access(self, vpn: Optional[bool] = None, admin: Optional[bool] = None) -> "EmployeeBuilder":
        if vpn is not None:
            self._d["has_vpn_access"] = vpn
        if admin is not None:
            self._d["has_admin_rights"] = admin
        return self

    def with_meta(self, manager_id: Optional[int] = None, office_location: Optional[str] = None,
                  contract_type: Optional[str] = None) -> "EmployeeBuilder":
        if manager_id is not None:
            self._d["manager_id"] = manager_id
        if office_location is not None:
            self._d["office_location"] = office_location
        if contract_type is not None:
            self._d["contract_type"] = contract_type
        return self

    def _validate(self) -> None:
        if not self._d.get("first_name") or not self._d.get("last_name"):
            raise ValueError("Name is required")
        email = self._d.get("email")
        if not email or "@" not in str(email):
            raise ValueError("Valid email is required")
        salary = self._d.get("salary")
        if salary is None or float(salary) < 0:
            raise ValueError("Salary cannot be negative")
        for k in ("department", "position", "start_date"):
            if not self._d.get(k):
                raise ValueError(f"{k} is required")

    def build(self) -> Employee:
        self._validate()
        return Employee(**self._d)


def developer_preset(builder: EmployeeBuilder) -> EmployeeBuilder:
    return builder.with_access(admin=True, vpn=True).with_equipment(laptop=True)


# Exercise 3

class ConfigSource(ABC):
    @abstractmethod
    def load(self) -> dict:
        raise NotImplementedError


class JsonFileConfigSource(ConfigSource):
    def __init__(self, path: str) -> None:
        self._path = path

    def load(self) -> dict:
        with open(self._path, "r", encoding="utf-8") as f:
            return json.load(f)


class ConfigManager:
    _instance: Optional["ConfigManager"] = None

    def __init__(self, source: ConfigSource) -> None:
        self._config = source.load()

    @classmethod
    def get_instance(cls, source: Optional[ConfigSource] = None) -> "ConfigManager":
        if cls._instance is None:
            if source is None:
                source = JsonFileConfigSource("config.json")
            cls._instance = cls(source)
        return cls._instance

    def get(self, key: str, default: Any = None) -> Any:
        current: Any = self._config
        for part in key.split("."):
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        return current
