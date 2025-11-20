# RGB to Pantone Color Converter

A Python program that converts RGB color codes to their closest Pantone color family equivalents.

## Features

- **Comprehensive Pantone Database**: Includes 70+ popular Pantone colors across all color families
- **Accurate Color Matching**: Uses Euclidean distance algorithm in RGB color space
- **Color Families**: Automatically identifies the color family (Red, Blue, Green, etc.)
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

The program recognizes the following Pantone color families:

- **Red Family**: PANTONE 185 C, 186 C, 187 C, 1788 C, 1795 C, etc.
- **Orange Family**: PANTONE 021 C, 151 C, 158 C, 165 C, etc.
- **Yellow Family**: PANTONE Yellow C, 100 C, 101 C, 109 C, etc.
- **Green Family**: PANTONE 347 C, 348 C, 354 C, Green C, etc.
- **Blue Family**: PANTONE 286 C, 285 C, 2925 C, Blue 072 C, etc.
- **Purple/Violet Family**: PANTONE 267 C, 268 C, 2592 C, Violet C, etc.
- **Pink Family**: PANTONE 213 C, 219 C, Pink C, Rhodamine Red C, etc.
- **Brown Family**: PANTONE 168 C, 4625 C, 7518 C, etc.
- **Gray Family**: Cool Gray and Warm Gray series
- **Black/White**: PANTONE Black C, Process Black C, White

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
- The database contains popular Pantone colors but not the complete Pantone library (thousands of colors)
- Color appearance can vary based on display calibration
- For professional color matching, always refer to official Pantone color guides

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
