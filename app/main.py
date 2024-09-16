from __future__ import annotations
from abc import ABC


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __get__(self, instance: any, owner: any) -> tuple:
        return self.min_amount, self.max_amount

    def __set__(self, instance: any, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Only integers are allowed")
        if value not in range(self.min_amount, self.max_amount + 1):
            raise ValueError(
                f"Value must be between "
                f"{self.min_amount} and {self.max_amount}"
            )
        setattr(instance, self.name, value)

    def __set_name__(self, owner: any, name: any) -> None:
        self.name = name


class Visitor:
    def __init__(self,
                 name: str,
                 age: int,
                 weight: int,
                 height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    def __init__(self,
                 age_range: IntegerRange,
                 weight_range: IntegerRange,
                 height_range: IntegerRange) -> None:
        self.age_range = age_range
        self.weight_range = weight_range
        self.height_range = height_range


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age_range=IntegerRange(4, 14),
            weight_range=IntegerRange(20, 50),
            height_range=IntegerRange(80, 120)
        )


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self) -> None:
        super().__init__(
            age_range=IntegerRange(14, 60),
            weight_range=IntegerRange(50, 120),
            height_range=IntegerRange(120, 220)
        )


class Slide:
    def __init__(self, name: str, limitation_class: type) -> None:
        self.name = name
        self.limitation_class = limitation_class()

    def can_access(self, visitor: Visitor) -> bool:
        try:
            return (
                self.limitation_class.age_range.min_amount
                <= visitor.age <= self.limitation_class.age_range.max_amount
                and self.limitation_class.weight_range.min_amount
                <= visitor.weight
                <= self.limitation_class.weight_range.max_amount
                and self.limitation_class.height_range.min_amount
                <= visitor.height
                <= self.limitation_class.height_range.max_amount
            )
        except Exception as e:
            print(e)
