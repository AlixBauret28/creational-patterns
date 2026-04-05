"""
Exercise 2: Builder Pattern — Employee Onboarding System

The Builder Pattern lets us construct complex objects step by step,
with readable chained method calls, instead of a massive constructor.
"""

from dataclasses import dataclass
from typing import Optional


# The final object we want to build.
# frozen=True means once created, it cannot be modified.

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


# The Builder: constructs an Employee piece by piece.
# Each method returns 'self' so we can chain calls.

class EmployeeBuilder:

    def __init__(self):
        self._data = {
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
        self._data["first_name"] = first_name
        self._data["last_name"] = last_name
        return self

    def with_email(self, email: str) -> "EmployeeBuilder":
        self._data["email"] = email
        return self

    def with_job(self, department: str, position: str, salary: float,
                 start_date: str) -> "EmployeeBuilder":
        self._data["department"] = department
        self._data["position"] = position
        self._data["salary"] = salary
        self._data["start_date"] = start_date
        return self

    def with_contact(self, phone: str = None, address: str = None,
                     emergency_contact: str = None) -> "EmployeeBuilder":
        if phone is not None:
            self._data["phone"] = phone
        if address is not None:
            self._data["address"] = address
        if emergency_contact is not None:
            self._data["emergency_contact"] = emergency_contact
        return self

    def with_equipment(self, laptop: bool = None,
                       parking: bool = None) -> "EmployeeBuilder":
        if laptop is not None:
            self._data["has_laptop"] = laptop
        if parking is not None:
            self._data["has_parking"] = parking
        return self

    def with_access(self, vpn: bool = None,
                    admin: bool = None) -> "EmployeeBuilder":
        if vpn is not None:
            self._data["has_vpn_access"] = vpn
        if admin is not None:
            self._data["has_admin_rights"] = admin
        return self

    def with_meta(self, manager_id: int = None, office_location: str = None,
                  contract_type: str = None) -> "EmployeeBuilder":
        if manager_id is not None:
            self._data["manager_id"] = manager_id
        if office_location is not None:
            self._data["office_location"] = office_location
        if contract_type is not None:
            self._data["contract_type"] = contract_type
        return self

    def _validate(self):
        """Make sure all required fields are present and valid."""
        if not self._data.get("first_name") or not self._data.get("last_name"):
            raise ValueError("First name and last name are required")

        email = self._data.get("email", "")
        if not email or "@" not in email:
            raise ValueError("A valid email is required")

        salary = self._data.get("salary")
        if salary is None or salary < 0:
            raise ValueError("Salary must be zero or positive")

        for field in ("department", "position", "start_date"):
            if not self._data.get(field):
                raise ValueError(f"{field} is required")

    def build(self) -> Employee:
        """Validate and create the final Employee object."""
        self._validate()
        return Employee(**self._data)


# A preset: pre-configures the builder for a developer role.
def developer_preset(builder: EmployeeBuilder) -> EmployeeBuilder:
    return builder.with_access(vpn=True, admin=True).with_equipment(laptop=True)


# --- Test it ---
if __name__ == "__main__":
    # Build a regular employee
    emp1 = (EmployeeBuilder()
            .with_name("Alice", "Martin")
            .with_email("alice.martin@company.com")
            .with_job("Marketing", "Analyst", 38000, "2026-05-01")
            .with_contact(phone="0601020304")
            .with_equipment(parking=True)
            .build())
    print("Employee 1:", emp1)
    print()

    # Build a developer using the preset
    builder = EmployeeBuilder()
    builder = (builder
               .with_name("Bob", "Leclerc")
               .with_email("bob.leclerc@company.com")
               .with_job("Engineering", "Backend Developer", 45000, "2026-04-15"))
    builder = developer_preset(builder)
    emp2 = builder.build()
    print("Employee 2:", emp2)
    print()

    # Try building with missing required fields
    try:
        bad = EmployeeBuilder().with_name("No", "Email").build()
    except ValueError as e:
        print("Validation error:", e)
