from dataclasses import dataclass


@dataclass
class FormField:
    
    selector: str
    tag: str
    input_type: str
    name: str
    placeholder: str
    label: str
    value: str
    required: bool
    visible: bool
