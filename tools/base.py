from dataclasses import dataclass, field
from typing import Literal, Any, Optional
import re


FieldType = Literal["text", "number", "select", "checkbox", "multiselect", "textarea", "file"]


@dataclass
class FieldOption:
    label: str
    value: str


@dataclass
class ToolField:
    name: str
    label: str
    type: FieldType
    required: bool = False
    placeholder: str = ""
    default: Any = None
    options: list[FieldOption] = field(default_factory=list)
    help: str = ""
    group: str = ""
    # Validation rules
    pattern: Optional[str] = None        # regex pattern (for text fields)
    pattern_msg: str = ""                # message shown when pattern fails
    min_val: Optional[float] = None      # min value (for number fields)
    max_val: Optional[float] = None      # max value (for number fields)
    min_select: Optional[int] = None     # min selections (for multiselect)


class Tool:
    name: str = ""
    description: str = ""
    category: str = ""
    icon: str = ""
    fields: list[ToolField] = []

    def build_command(self, params: dict) -> list[str]:
        raise NotImplementedError

    def validate(self, params: dict) -> list[str]:
        """Validate params against field rules. Returns list of error messages."""
        errors = []
        for f in self.fields:
            val = params.get(f.name)

            # Required check
            if f.required:
                empty = (
                    val is None or
                    (isinstance(val, str) and not val.strip()) or
                    (isinstance(val, list) and len(val) == 0)
                )
                if empty:
                    errors.append(f"«{f.label}» es obligatorio.")
                    continue  # no point checking further rules

            # Skip further validation if empty and not required
            if val is None or val == "" or val == []:
                continue

            # Pattern check (text fields)
            if f.pattern and isinstance(val, str) and val.strip():
                if not re.fullmatch(f.pattern, val.strip()):
                    msg = f.pattern_msg or f"«{f.label}» tiene un formato inválido."
                    errors.append(msg)

            # Number range checks
            if f.type == "number" and val != "":
                try:
                    n = float(val)
                    if f.min_val is not None and n < f.min_val:
                        errors.append(f"«{f.label}» debe ser ≥ {f.min_val}.")
                    if f.max_val is not None and n > f.max_val:
                        errors.append(f"«{f.label}» debe ser ≤ {f.max_val}.")
                except (ValueError, TypeError):
                    errors.append(f"«{f.label}» debe ser un número.")

            # Multiselect minimum
            if f.type == "multiselect" and f.min_select and isinstance(val, list):
                if len(val) < f.min_select:
                    errors.append(f"«{f.label}»: selecciona al menos {f.min_select} opción(es).")

        return errors

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "icon": self.icon,
            "fields": [
                {
                    "name": f.name,
                    "label": f.label,
                    "type": f.type,
                    "required": f.required,
                    "placeholder": f.placeholder,
                    "default": f.default,
                    "options": [{"label": o.label, "value": o.value} for o in f.options],
                    "help": f.help,
                    "group": f.group,
                    "pattern": f.pattern,
                    "pattern_msg": f.pattern_msg,
                    "min_val": f.min_val,
                    "max_val": f.max_val,
                    "min_select": f.min_select,
                }
                for f in self.fields
            ],
        }
