from weatherclock.settings.icon_map import ICON_MAP
from PIL import Image, ImageDraw, ImageFont

font_fpath: str = "/System/Library/Fonts/Supplemental/Arial.ttf"

font = ImageFont.truetype(font_fpath, 14)
unpadded: Image = Image.open("icons/png/wi-cloud-2.0.png")
padded: Image = Image.new(
    unpadded.mode,
    (unpadded.size[0], unpadded.size[1] + unpadded.size[1] // 4),
    (0, 0, 0, 0),
)
padded.paste(unpadded, (0, 0))

draw: ImageDraw = ImageDraw.Draw(padded)
draw.text(
    (padded.size[0] // 2, unpadded.size[1]),  #  + unpadded.size[1] // 8
    "64\u00b0 | 5%",
    fill="black",
    anchor="ms",
    font=font,
)
print(padded.size)
# padded.show()


class HourMarkers:
    def __init__(self, hourly_forecast_abbreviations: list[tuple[str, str]]) -> None:
        # Look up the icons from the icon map
        # Input: list of (short forecast, day/night) tuples
        self.icons: list = list(range(1, 13))