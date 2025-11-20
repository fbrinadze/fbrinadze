# RGB to Pantone Color Converter

A Python program that converts RGB color codes to their closest Pantone color family equivalents.

## Features

- **COMPREHENSIVE Pantone Database**: Includes **473 Pantone colors** across ALL color families
- **Accurate Color Matching**: Uses Euclidean distance algorithm in RGB color space
- **15+ Color Families**: Automatically identifies the color family (Red, Pink, Magenta, Purple, Blue, Teal, Green, Yellow, Orange, Brown, Gray, Metallic, Neon, Pastel, and more)
- **Multiple Matches**: Can display top N closest matches
- **Similarity Percentage**: Shows how closely the RGB matches the Pantone color
- **Easy CLI Interface**: Simple command-line usage

## Installation

No additional dependencies required! The program uses only Python standard library.

```bash
# Make the script executable (optional)
chmod +x rgb_to_pantone.py
```

## Usage

### Basic Usage

Convert an RGB color to its closest Pantone match:

```bash
python rgb_to_pantone.py <R> <G> <B>
```

**Example:**
```bash
python rgb_to_pantone.py 255 0 0
```

Output:
```
============================================================
RGB TO PANTONE CONVERTER
============================================================
Input: RGB(255, 0, 0)
Finding top 1 Pantone match(es)...

============================================================
BEST MATCH:
============================================================
Pantone Color:    PANTONE 185 C
Color Family:     Red Family
Input RGB:        RGB(255, 0, 0)
Pantone RGB:      RGB(228, 0, 43)
Distance:         50.66
Similarity:       88.5%
```

### Show Multiple Matches

Use the `-t` or `--top` flag to show multiple closest matches:

```bash
python rgb_to_pantone.py 100 150 200 --top 3
```

or

```bash
python rgb_to_pantone.py 100 150 200 -t 3
```

## Examples

### Example 1: Pure Red
```bash
python rgb_to_pantone.py 255 0 0
```

### Example 2: Sky Blue
```bash
python rgb_to_pantone.py 135 206 235 --top 5
```

### Example 3: Forest Green
```bash
python rgb_to_pantone.py 34 139 34 -t 3
```

### Example 4: Purple
```bash
python rgb_to_pantone.py 128 0 128
```

## Color Families Included

The program recognizes **15+ Pantone color families** with extensive coverage:

### Primary Color Families
- **Red Family** (32 colors): PANTONE 179-202 C, 1767-1817 C series, Red 032 C
- **Pink Family** (32 colors): PANTONE 176-232 C, Pink C, Rhodamine Red C
- **Magenta Family** (12 colors): PANTONE 233-251 C
- **Purple/Violet Family** (33 colors): PANTONE 252-272 C, 2562-2695 C series, Violet C, Purple C
- **Blue Family** (30 colors): PANTONE 278-306 C, 2706-2945 C series, Blue 072 C, Reflex Blue C, Process Blue C
- **Teal/Aqua Family** (28 colors): PANTONE 310-330 C, 7466-7471 C, 7687-7689 C, 801-803 C, Teal C
- **Green Family** (48 colors): PANTONE 331-378 C, Green C
- **Yellow Family** (35 colors): PANTONE 100-134 C, Yellow C, Yellow 012 C
- **Orange Family** (41 colors): PANTONE 021 C, 135-169 C, 1575-1625 C series, Orange 021 C

### Earth Tones & Neutrals
- **Brown/Tan Family** (89 colors): PANTONE 462-482 C, 4625-4685 C, 7499-7587 C series
- **Gray Family** (28 colors): Cool Gray 1-11 C, Warm Gray 1-11 C, Black 2-7 C
- **Black Family** (2 colors): PANTONE Black C, Process Black C
- **White Family** (1 color): PANTONE White

### Special Color Families
- **Metallic Family** (7 colors): PANTONE 871-877 C (gold and silver tones)
- **Neon/Fluorescent Family** (5 colors): PANTONE 804-808 C
- **Pastel Family** (18 colors): PANTONE 9060-9162 C series

## How It Works

1. **Input Validation**: Ensures RGB values are in the valid range (0-255)
2. **Distance Calculation**: Computes Euclidean distance between input RGB and each Pantone color
3. **Matching**: Finds the closest Pantone color(s) based on minimum distance
4. **Family Classification**: Determines the color family of the matched Pantone color
5. **Results**: Displays detailed information including similarity percentage

## Algorithm

The program uses the Euclidean distance formula in RGB color space:

```
distance = √[(R₂-R₁)² + (G₂-G₁)² + (B₂-B₁)²]
```

The similarity percentage is calculated as:

```
similarity = 100 × (1 - distance / max_distance)
```

where `max_distance = √(255² + 255² + 255²) ≈ 441.67`

## Limitations

- RGB to Pantone conversion is approximate since Pantone colors are defined for physical printing
- The database contains **473 carefully selected Pantone colors** representing all major families, but not the complete Pantone library (which contains thousands of colors including specialty inks)
- Color appearance can vary based on display calibration and monitor settings
- RGB values provided are approximations for digital use and may not exactly match physical Pantone swatches
- For professional color matching and print production, always refer to official Pantone color guides and physical swatch books

## Use as a Python Module

You can also import and use the functions in your own Python code:

```python
from rgb_to_pantone import rgb_to_pantone, get_color_family

# Get the closest Pantone match
matches = rgb_to_pantone(255, 0, 0, top_n=1)
pantone_name, pantone_rgb, distance = matches[0]

print(f"Closest Pantone: {pantone_name}")
print(f"Color Family: {get_color_family(pantone_name)}")

# Get top 5 matches
top_5 = rgb_to_pantone(100, 150, 200, top_n=5)
for name, rgb, dist in top_5:
    print(f"{name}: {rgb} (distance: {dist:.2f})")
```

## License

This is a utility tool for educational and reference purposes.

## Notes

- Pantone® is a registered trademark of Pantone LLC
- RGB values are approximations of Pantone colors for digital use
- For critical color matching in professional printing, consult official Pantone guides
