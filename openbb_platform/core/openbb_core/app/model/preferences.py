"""Preferences for the OpenBB platform."""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class Preferences(BaseModel):
    """Preferences for the OpenBB platform."""

    cache_directory: str = str(Path.home() / "OpenBBUserData" / "cache")
    chart_style: Literal["dark", "light"] = "dark"
    data_directory: str = str(Path.home() / "OpenBBUserData")
    export_directory: str = str(Path.home() / "OpenBBUserData" / "exports")
    metadata: bool = True
    output_type: Literal[
        "OBBject", "dataframe", "polars", "numpy", "dict", "chart", "llm"
    ] = Field(
        default="OBBject",
        description="Python default output type.",
        validate_default=True,
    )
    plot_enable_pywry: bool = True
    plot_open_export: bool = (
        False  # Whether to open plot image exports after they are created
    )
    plot_pywry_height: PositiveInt = 762
    plot_pywry_width: PositiveInt = 1400
    request_timeout: PositiveInt = 60
    show_warnings: bool = True
    table_style: Literal["dark", "light"] = "dark"
    user_styles_directory: str = str(Path.home() / "OpenBBUserData" / "styles" / "user")

    model_config = ConfigDict(validate_assignment=True)

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"{self.__class__.__name__}\n\n" + "\n".join(
            f"{k}: {v}" for k, v in self.model_dump().items()
        )