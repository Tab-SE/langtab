from langserve.serialization import WellKnownLCSerializer
import pandas as pd
from typing import Any


class CustomSerializer(WellKnownLCSerializer):
    """
    Override and customize Langserve serialization behavior
    to add support for:
    - Dataframes used by the Pandas Agent
    """

    def dumps(self, obj: Any) -> bytes:
        """Override dumps to handle DataFrames."""
        if isinstance(obj, pd.DataFrame):
            return super().dumps(obj.to_dict(orient='records'))  # Convert DataFrame to dict
        return super().dumps(obj)

    def loadd(self, s: bytes) -> Any:
        """Override loadd if you need custom deserialization logic."""
        return super().loadd(s)
