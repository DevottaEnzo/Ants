# Langton's Ant Lab

A single-file browser app (`index.html`, no build step, no dependencies) that runs Langton's ant, styled as one realistic hardware device: a recessed screen above a row of twelve bat-handle toggle switches, then an aluminium speed knob, an LCD readout (rule and steps/s) and a latching run button with a status LED. `langtons_ant.py` is the earlier command-line version that writes a PNG with Pillow.

## Run

Open `index.html` in a browser, or serve the folder: `python3 -m http.server 8000`.

## How it works

- Flip switches have three positions: up = `L`, middle = off, down = `R`. The rule is the on switches read left to right (off ones skipped), so 12 switches give rules of up to 12 colours (e.g. `RRLLLRLLLRRR`). Default is `R L` + ten off = the classic `RL` ant.
- Each switch's lever cap shows the colour it controls; in the centre (off) position the lever points at the viewer and shows a dark cap. Flipping L↔R changes the turn live; turning a switch on or off changes the colour count, so the screen clears. All switches off = idle.
- Speed knob: float value 0–100 maps exponentially to `RATE_MIN`–`RATE_MAX` steps per second (2–600,000; default 60 ≈ 3,900/s). The loop accumulates `rate × dt`, so speed is independent of refresh rate and takes effect on the next frame. Turning: drag around the knob (angle-based, 270° = full range), press on the printed scale to jump to that mark, near the centre a plain up/right drag; also wheel/trackpad (proportional to delta) and arrow keys.
- Grid is fixed at 200×280 (5:7, matching the screen), edges wrap. A `Uint8Array` holds colour indices; a `Uint32Array` view over an `ImageData` buffer holds the pixels, so each step updates one cell and one pixel.
- Camera: `run()` tracks the bounding box of every cell visited; each frame the view eases (log-space zoom, `CAM_TAU`) toward that box plus `CAM_PAD`, never tighter than `CAM_MIN` cells, clamped to the grid. A fresh grid starts zoomed in on the ant. The view canvas is sized to its CSS box × devicePixelRatio and draws the 200×280 offscreen canvas with nearest-neighbour scaling; a faint cell grid fades in when zoomed close.
- Hardware look: switch gradients and drop shadows live in one shared hidden `<svg><defs>`; the knob is CSS (knurled `repeating-conic-gradient` skirt that rotates, static brushed-metal cap so the lighting stays fixed).
- Colours 0 and 1 come from `--ink0` / `--ink1` and follow light/dark mode; colours 2–11 are fixed accents (`ACCENTS`).

## Conventions

- Keep it one self-contained file. The only external request is the Google Fonts stylesheet; system fonts are the fallback.
- Colours are CSS custom properties in `:root`, with light and dark themes.
- The `.machine` element is a size container; everything inside is sized in `cqw` so the device scales as one piece. Its width is capped by viewport height (machine height ≈ 1.8 × width) so it fits on both phones and desktops.
- Switches and the knob are `role="slider"` with keyboard support; keep that when changing them.

## Ideas to extend

- Bring back PNG export (removed in the machine redesign) as a hardware-style button.
- A reset control that doesn't require toggling a switch.
- Multiple ants, or turmites with state tables.
- Hex or triangular grids.
- Save and load rule sets in `localStorage`.
- Share a rule and colours through the URL hash.
- Move the simulation to a Web Worker for faster jumps.
