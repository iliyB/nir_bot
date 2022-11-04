from dataclasses import dataclass
from typing import Optional


@dataclass
class ObservedStrObject:
    main_info: Optional[str] = None
    extract_info: Optional[str] = None
    cars_info: Optional[str] = None
    delivery_info: Optional[str] = None
