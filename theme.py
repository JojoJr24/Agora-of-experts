from __future__ import annotations
from typing import Iterable
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes


class AoeTheme(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.green,
        secondary_hue: colors.Color | str = colors.lime,
        neutral_hue: colors.Color | str = colors.neutral,
        spacing_size: sizes.Size | str = sizes.spacing_sm,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_lg,
        font: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("Quicksand"),
            "ui-sans-serif",
            "sans-serif",
        ),
        font_mono: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("IBM Plex Mono"),
            "ui-monospace",
            "monospace",
        ),
    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,
            font_mono=font_mono,
        )
        super().set(
            body_background_fill="repeating-linear-gradient(45deg, *neutral_200, *neutral_200 10px, *neutral_100 10px, *neutral_100 20px)",
            body_background_fill_dark="repeating-linear-gradient(45deg, *neutral_800, *neutral_800 10px, *neutral_900 10px, *neutral_900 20px)",
            slider_color="*secondary_300",
            slider_color_dark="*secondary_600",
            block_title_text_weight="600",
            block_border_width="2px",
            block_shadow="*shadow_drop_md",
            button_shadow="*shadow_drop_md",
            button_large_padding="8px",
            
        )


