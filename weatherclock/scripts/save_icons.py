import os
import sys
import cairosvg

from weatherclock.settings.icon_map import ICON_MAP


def purge(keep_icon_fpaths: list[str]) -> None:
    all_icons_fpaths: list[str] = [
        f"icons/svg/{fname}" for fname in os.listdir("icons/svg")
    ]
    for icon_fpath in all_icons_fpaths:
        if icon_fpath not in keep_icon_fpaths:
            os.remove(icon_fpath)


if __name__ == "__main__":
    args: list[str] = sys.argv[1:]
    scale: float = float(args[0])
    if len(args) == 0:
        print("Usage: python -m scripts.save_icons.py scale [purge]")
        sys.exit(1)
    purge_svgs: bool = True if len(args) == 2 and args[1] == "purge" else False

    keep_icon_names: list[str] = list(
        set(
            [v["day"] for v in ICON_MAP.values()]
            + [v["night"] for v in ICON_MAP.values()]
        )
    )

    keep_icon_fpaths: list[str] = [
        f"icons/svg/{icon_name}.svg" for icon_name in keep_icon_names
    ]

    if purge_svgs:
        purge(keep_icon_fpaths)

    for icon_name in keep_icon_names:
        cairosvg.svg2png(
            url=f"icons/svg/{icon_name}.svg",
            write_to=f"icons/png/{icon_name}-{scale}.png",
            scale=scale,
        )
