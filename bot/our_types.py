from dataclasses import dataclass
from typing import Optional


@dataclass
class ObservedStrObject:
    main_info: Optional[str] = None
    extract_info: Optional[str] = None
    cars_info: Optional[str] = None
    delivery_info: Optional[str] = None

    @property
    def get_all_card(self) -> str:
        return (
            str(self.main_info)
            + str(self.extract_info)
            + str(self.cars_info)
            + str(self.delivery_info)
        )
