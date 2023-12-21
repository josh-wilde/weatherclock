# weatherclock

Raspberry Pi WeatherClock

# Environments

- `env` environment from `requirements.txt` on pi and remote

## Displays

- [5.7" almost square eink](https://www.pishop.us/product/inky-impression-5-7-7-colour-epaper-eink-hat/)
- [7" official RPi touchscreen](https://www.pishop.us/product/official-raspberry-pi-7-touch-screen-display-with-10-finger-capacitive-touch/?src=raspberrypi)

## Plan for the icons

1. The hourly forecast has an "icon" entry. (e.g. "https://api.weather.gov/icons/land/night/bkn,14?size=small")
2. In the [icons page](https://api.weather.gov/icons), there is a map from the three letter code "bkn" to a short description, "Mostly cloudy".
3. I should be able to map the short descriptions plus the day/night indication (either isDaytime in the hourly forecast, or parse the icon again) to [new icons](https://erikflowers.github.io/weather-icons/). I can take the SVG images from this repo.
4. It doesn't seem that Python is able to handle SVG files well. Might have to convert them to a different format using [CairoSVG](https://cairosvg.org/) or something else.

## Using matplotlib for the image display

- [This snippet](https://gist.githubusercontent.com/Kopfgeldjaeger/45b4cb02c48921a8ab238754c1034647/raw/a48c20a27f0ed7bc29be8c5c65240272df545745/dynamic_clock) uses matplotlib to display a clock with an animation.
- Looks like it is possible to replace the axis ticks with images, see an example [here](https://stackoverflow.com/questions/69538086/how-to-use-images-as-xtick-labels-in-seaborn-matplotlib-barplot) and [here](https://stackoverflow.com/questions/44246650/add-image-annotations-to-bar-plots).

## Design

Maybe the clock with icons and temps/precip on the left, and on the right, big bold date and the `detailedForecast` readout from the [forecast](https://api.weather.gov/gridpoints/BOX/64,86/forecast) below that.

## Code design

The main loop needs to `plt.show()` a single `FunctionAnimation` object (`animation`).
The figure input into `animation` is the full display figure, with 3 subplots.
The update function should be a driver of multiple updates for all three subplots.

Not sure about wrappers for the subplots yet.
Might be helpful to take in relevant parameters and construct the `matplotlib` object that goes into the figure.
Will need to figure out if this will work with variable scope.

- Entire display is a `Display` that holds a `matplotlib` object with three subplots - left, top right, bottom right.
  - The right two subplots are `TextBox` objects.
  - The left subplot is a `WeatherClock` object.
- `Display`
  - Wraps a `matplotlib` figure with set number of subplots and sizes for these subplots.
- `TextBox`
  - Input text and `matplotlib` parameters and get a text subplot.
  - Maybe a `Date` object inherits from this and has an update function to generate the text.
- `WeatherClock`
  - A single `matplotlib` subplot that is an animated clock and
