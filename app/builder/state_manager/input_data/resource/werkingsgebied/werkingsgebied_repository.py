import uuid
from typing import Dict, List, Optional

from app.builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied


class WerkingsgebiedRepository:
    def __init__(self, provincie_id: str, expression_taal: str):
        self._provincie_id: str = provincie_id
        self._expression_taal: str = expression_taal
        self._werkingsgebieden: Dict[str, Werkingsgebied] = {}

    def add(self, werkingsgebied: dict):
        werkingsgebied_id = werkingsgebied["UUID"]
        werkingsgebied["provincie_id"] = self._provincie_id
        werkingsgebied["expression_taal"] = self._expression_taal
        self._werkingsgebieden[werkingsgebied_id] = Werkingsgebied.model_validate(werkingsgebied)

    def add_list(self, werkingsgebieden: List[dict]):
        for werkingsgebied in werkingsgebieden:
            self.add(werkingsgebied)

    def get_optional(self, idx: uuid.UUID) -> Optional[Werkingsgebied]:
        werkingsgebied: Optional[Werkingsgebied] = self._werkingsgebieden.get(str(idx))
        return werkingsgebied

    def get(self, idx: uuid.UUID) -> Werkingsgebied:
        werkingsgebied: Optional[Werkingsgebied] = self.get_optional(idx)
        if werkingsgebied is None:
            raise RuntimeError(f"Can not find werkingsgebied {idx}")
        return werkingsgebied

    def all(self) -> List[Werkingsgebied]:
        return list(self._werkingsgebieden.values())

    def is_empty(self) -> bool:
        return not self._werkingsgebieden
