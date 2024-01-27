from weatherclock.settings.icon_map import ICON_MAP
from PIL import Image, ImageDraw, ImageFont

# TODO: probably when resetting all of the images, I should close the existing ones first.
# Maybe optimize so that the ones that don't change aren't closed and reopened

# TODO: need to fix the input types and parse the icon_url with the icon map


class HourMarkers:
    def __init__(
        self, hourly_forecast_abbreviations: dict[int, tuple[str, str]] | None = None
    ) -> None:
        # Look up the icons from the icon map
        # Input: dict of hour_num: (short forecast, day/night) tuples
        self.icons: list[Image.Image] = []
        self.update(hourly_forecast_abbreviations)

    def update(self, hourly_forecast: list[tuple[str, str]] | None) -> None:
        # Grab the icon and add padding space for the text
        unpadded: Image.Image = Image.open("icons/png/wi-day-sunny-1.75.png")
        padded: Image.Image = Image.new(
            unpadded.mode,
            (unpadded.size[0], unpadded.size[1] + unpadded.size[1] // 4),
            (0, 0, 0, 0),
        )
        padded.paste(unpadded, (0, 0))

        # Add text
        font_fpath: str = "/Users/jwilde/Library/Fonts/Quicksand-Regular.ttf"
        font: ImageFont.FreeTypeFont = ImageFont.truetype(font_fpath, 10)
        draw: ImageDraw.ImageDraw = ImageDraw.Draw(padded)
        draw.text(
            (
                padded.size[0] // 2,
                unpadded.size[1] + unpadded.size[1] // 8,
            ),
            "105\u00b0 | 100%",
            fill="black",
            anchor="ms",
            font=font,
        )

        # Set the icons
        self.icons = [padded.copy() for _ in range(12)]

    def get_icons(self) -> list[Image.Image]:
        return self.icons
