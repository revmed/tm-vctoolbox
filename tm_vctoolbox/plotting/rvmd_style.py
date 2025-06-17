"""
rvmd_style.py

Defines custom fonts, color palettes, and matplotlib themes for the RVMD project.

- Registers company-specific fonts (FKGroteskNeue and FKGroteskNeueBold).
- Provides predefined RVMD color palettes for consistent branding.
- Implements reusable matplotlib style configurations to ensure consistent
  appearance across visualizations.

Usage:
    from rvmd_style import RVMDStyle

    style = RVMDStyle()
    style.apply_theme()
"""

# %%
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

from tm_vctoolbox.utils import get_current_dir


# %%
@dataclass
class RVMDStyle:
    font_dir: Path = Path(get_current_dir()) / "fonts"
    font_regular_name: str = "FKGroteskNeue"
    font_bold_name: str = "FKGroteskNeueBold"
    font_regular_file: Path = field(init=False)
    font_bold_file: Path = field(init=False)

    primary_palette: List[str] = field(
        default_factory=lambda: [
            "#1E6B5C",
            "#70FFE5",
            "#13D377",
            "#0E4343",
            "#56716C",
            "#F2F2F2",
            "#FFFFFF",
        ]
    )

    def __post_init__(self):
        self.font_regular_file = self.font_dir / f"{self.font_regular_name}.ttf"
        self.font_bold_file = self.font_dir / f"{self.font_bold_name}.ttf"
        self.font_dash_bold_file = self.font_dir / f"{self.font_regular_name}-Bold.ttf"
        self._register_fonts()

    def _register_fonts(self):
        fm.fontManager.addfont(str(self.font_regular_file))
        fm.fontManager.addfont(str(self.font_bold_file))
        fm.fontManager.addfont(str(self.font_dash_bold_file))
        plt.rcParams["font.family"] = self.font_regular_name

    def apply_theme(self):
        plt.rcParams.update(
            {
                "font.family": self.font_regular_name,
                "axes.titlesize": 24,
                "axes.labelsize": 20,
                "xtick.labelsize": 18,
                "ytick.labelsize": 18,
                "legend.fontsize": 18,
                "axes.edgecolor": "black",
                "axes.linewidth": 1.2,
                "xtick.major.size": 6,
                "ytick.major.size": 6,
                "legend.frameon": False,
                "figure.facecolor": "white",
                "axes.facecolor": "white",
            }
        )


@dataclass
class RVMDColorPalettes:
    rvmd_color_palette_primary: List[str] = field(
        default_factory=lambda: [
            "#1E6B5C",
            "#70FFE5",
            "#13D377",
            "#0E4343",
            "#56716C",
            "#F2F2F2",
            "#FFFFFF",
        ]
    )
    rvmd_color_palette_secondary_light: List[str] = field(
        default_factory=lambda: ["#D1A6FF", "#8D9BFF", "#FF9966", "#FFCD69"]
    )
    rvmd_color_palette_secondary_medium: List[str] = field(
        default_factory=lambda: ["#A24DFF", "#5136E0", "#FF5400", "#FFAA00"]
    )
    rvmd_color_palette_secondary_dark: List[str] = field(
        default_factory=lambda: ["#5C2C91", "#2B1980", "#C44202", "#C28100"]
    )
    rvmd_color_palette_pk_6236: List[str] = field(
        default_factory=lambda: [
            "#8D9BFF",
            "#5136E0",
            "#2B1980",
            "#DADADA",
            "#56716C",
            "#70FFE5",
            "#39BC69",
            "#2B9259",
            "#104343",
        ]
    )
    rvmd_color_palette_pk_6291: List[str] = field(
        default_factory=lambda: [
            "#8D9BFF",
            "#5136E0",
            "#2B1980",
            "#70FFE5",
            "#39BC69",
            "#2B9259",
            "#104343",
        ]
    )
    rvmd_color_palette_pk_9805_indication: List[str] = field(
        default_factory=lambda: [
            "#1B9E77",
            "#D95F02",
            "#7570B3",
            "#E7298A",
            "#66A61E",
            "#E6AB02",
            "#A6761D",
            "#666666",
        ]
    )
    rvmd_color_palette_pk_9805_indication_order: List[str] = field(
        default_factory=lambda: ["PDAC", "NSCLC", "CRC", "OTHER"]
    )
    rvmd_color_palette_pk_9805_indication_4: List[str] = field(
        default_factory=lambda: ["#1B9E77", "#D95F02", "#7570B3", "#E7298A"]
    )
    rvmd_color_palette_pk_9805_dose: List[str] = field(
        default_factory=lambda: [
            "#a6cee3",
            "#1f78b4",
            "#b2df8a",
            "#33a02c",
            "#104343",
            "#FF01FF",
            "#FF0190",
            "#B29DBD",
            "#6a3d9a",
            "#C28100",
            "#FF9966",
            "#FF01FF",
            "#FF0190",
        ]
    )
    rvmd_color_palette_pk_9805_dose_600: List[str] = field(
        default_factory=lambda: [
            "#b2df8a",
            "#33a02c",
            "#FF01FF",
            "#FF0190",
            "#B29DBD",
            "#6a3d9a",
        ]
    )
    rvmd_color_palette_pk_9805_dose_900: List[str] = field(
        default_factory=lambda: ["#FF01FF", "#FF0190", "#B29DBD", "#6a3d9a"]
    )
    rvmd_color_palette_pk_9805_dose_1200: List[str] = field(
        default_factory=lambda: ["#B29DBD", "#6a3d9a"]
    )
    rvmd_color_palette_pk_9805_dose_order: List[str] = field(
        default_factory=lambda: [
            "150 mg QD",
            "300 mg QD",
            "600 mg QD",
            "300 mg BID",
            "900 mg QD",
            "450 mg BID",
            "1200 mg QD",
            "600 mg BID",
            "100 mg 6236, 600 mg 9805",
            "100 mg 6236, 900 mg 9805",
            "100 mg 6236, 1200 mg 9805",
            "200 mg 6236, 1200 mg 9805",
            "300 mg 6236, 1200 mg 9805",
            "NA",
        ]
    )
    rvmd_color_palette_pk_9805_bor_order: List[str] = field(
        default_factory=lambda: ["CR/CRu", "PR/PRu", "SD", "PD", "NE"]
    )
    rvmd_color_palette_pk_9805_bor: List[str] = field(
        default_factory=lambda: [
            "#C7EDFD",
            "#4699C7",
            "#a9ff00",
            "#A7D24F",
            "#87A14C",
            "#5B722B",
        ]
    )


# %%
