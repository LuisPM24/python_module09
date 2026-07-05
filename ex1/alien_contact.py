from enum import Enum
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError
from pydantic import model_validator  # type: ignore


class ContactType(Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(..., max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_aliencontact(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Invalid data - Contact ID must start with 'AC'")
        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Invalid data - Physical contact is not verified")
        if (
            self.contact_type == ContactType.telepathic and
            self.witness_count < 3
           ):
            raise ValueError("Invalid data - No enough witnesses on telephatic"
                             " contact")
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Invalid data - Strong signals ( > 7.0 ) needs a "
                             "received message")
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================\n")
    try:
        alien_contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2024, 1, 1, 18, 32, 0),
            location="Area 51, Nevada",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli"
        )

        print("Valid contact report:")
        print(f"ID: {alien_contact.contact_id}")
        print(f"Type: {alien_contact.contact_type}")
        print(f"Location: {alien_contact.location}")
        print(f"Signal: {alien_contact.signal_strength}/10")
        print(f"Duration: {alien_contact.duration_minutes} minutes")
        print(f"Witnesses: {alien_contact.witness_count}")
        print(f"Message: '{alien_contact.message_received}'")
    except ValidationError as e:
        print(f"Expected error: {e}")

    print("\n======================================\n")

    try:
        broken_contact = AlienContact(
            contact_id="AC2024_001",
            timestamp=datetime(2024, 1, 1, 18, 32, 0),
            location="Area 51, Nevada",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received=""
        )

        print("Valid contact report:")
        print(f"ID: {broken_contact.contact_id}")
        print(f"Type: {broken_contact.contact_type}")
        print(f"Location: {broken_contact.location}")
        print(f"Signal: {broken_contact.signal_strength}/10")
        print(f"Duration: {broken_contact.duration_minutes} minutes")
        print(f"Witnesses: {broken_contact.witness_count}")
        print(f"Message: '{broken_contact.message_received}'")
    except ValidationError as e:
        print(f"Expected error: {e}")


if __name__ == "__main__":
    main()
