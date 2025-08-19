from typing import Annotated

from ocelescope import OCEL, OCELAnnotation, Plugin, plugin_method

from .inputs.example import ExampleInput
from .resources.example import ExampleResource


class Totem(Plugin):
    label = "TOTeM"
    description = "Generate Temporal Object Type Models (TOTeM) to uncover type-level temporal and cardinality relations in event logs"
    version = "0.1.0"

    @plugin_method(label="Example Method", description="An example plugin method")
    def example(
        self,
        ocel: Annotated[OCEL, OCELAnnotation(label="Event Log")],
        input: ExampleInput,
    ) -> ExampleResource:
        return ExampleResource()
