from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ValidationError


class Rank(Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def mission_validation(self) -> "SpaceMission":
        leader: bool = False
        experienced_crew: int = 0

        if not self.mission_id.startswith("M"):
            raise ValueError("Error - Mission ID don't start with 'M' char")
        for member in self.crew:
            if member.rank == Rank.commander or member.rank == Rank.captain:
                leader = True
            if member.years_experience >= 5:
                experienced_crew += 1
            if member.is_active is False:
                raise ValueError("Error - Inactives members inside the crew")
        if leader is False:
            raise ValueError("Error - No commander or captain inside the crew")
        if (
            (experienced_crew / len(self.crew)) * 100 < 50.0 and
            self.duration_days > 365
           ):
            raise ValidationError("Error - Not enough experienced tripulation")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================\n")
    crew_members1: list[CrewMember] = [
        CrewMember(
            member_id="123",
            name="Sara Connor",
            rank=Rank.commander,
            age=42,
            specialization="Mission Command",
            years_experience=7,
            is_active=True
        ),
        CrewMember(
            member_id="234",
            name="John Smith",
            rank=Rank.lieutenant,
            age=33,
            specialization="Navigation",
            years_experience=6,
            is_active=True
        ),
        CrewMember(
            member_id="345",
            name="Alice Johnson",
            rank=Rank.officer,
            age=27,
            specialization="Engineering",
            years_experience=2,
            is_active=True
        )
    ]
    try:
        mission = SpaceMission(
            mission_id="Mars Colony",
            mission_name="M2026_MARS",
            destination="Mars",
            launch_date=datetime(2026, 7, 7, 12, 47, 30),
            duration_days=900,
            crew=crew_members1,
            mission_status="Active",
            budget_millions=2500.0
        )
        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])

    try:
        print("\n=========================================\n")
        crew_members1[0].rank = Rank.officer
        mission = SpaceMission(
            mission_id="Mars Colony",
            mission_name="M2026_MARS",
            destination="Mars",
            launch_date=datetime(2026, 7, 7, 12, 47, 30),
            duration_days=900,
            crew=crew_members1,
            mission_status="Active",
            budget_millions=2500.0
        )
        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")
    except ValidationError as e:
        print("Expected validation error:")
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
