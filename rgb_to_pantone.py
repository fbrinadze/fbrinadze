#!/usr/bin/env python3
"""
RGB to Pantone Color Converter

This program converts RGB color codes to their closest Pantone color family equivalents.
It uses Euclidean distance in RGB color space to find the nearest match.
"""

import math
import argparse
from typing import Tuple, Dict, List


# Pantone color database with RGB approximations
# Format: {Pantone Name: (R, G, B)}
PANTONE_COLORS = {
    # Reds
    "PANTONE 185 C": (228, 0, 43),
    "PANTONE 186 C": (200, 16, 46),
    "PANTONE 187 C": (167, 25, 48),
    "PANTONE 1788 C": (228, 0, 69),
    "PANTONE 1795 C": (228, 0, 127),
    "PANTONE 1805 C": (228, 85, 133),
    "PANTONE Red 032 C": (239, 51, 64),

    # Oranges
    "PANTONE 021 C": (254, 80, 0),
    "PANTONE 151 C": (255, 104, 31),
    "PANTONE 158 C": (255, 103, 31),
    "PANTONE 165 C": (255, 94, 0),
    "PANTONE 1575 C": (255, 109, 0),
    "PANTONE 1585 C": (255, 99, 25),
    "PANTONE Orange 021 C": (254, 80, 0),

    # Yellows
    "PANTONE Yellow C": (254, 221, 0),
    "PANTONE 100 C": (244, 237, 98),
    "PANTONE 101 C": (244, 237, 71),
    "PANTONE 102 C": (254, 228, 64),
    "PANTONE 109 C": (255, 214, 0),
    "PANTONE 116 C": (255, 200, 8),
    "PANTONE 123 C": (255, 188, 0),

    # Greens
    "PANTONE 347 C": (0, 143, 81),
    "PANTONE 348 C": (0, 135, 68),
    "PANTONE 349 C": (0, 119, 73),
    "PANTONE 354 C": (0, 175, 102),
    "PANTONE 355 C": (0, 158, 96),
    "PANTONE 356 C": (0, 142, 91),
    "PANTONE 364 C": (103, 194, 58),
    "PANTONE 375 C": (139, 198, 63),
    "PANTONE Green C": (0, 173, 131),

    # Blues
    "PANTONE 286 C": (0, 45, 114),
    "PANTONE 285 C": (0, 57, 166),
    "PANTONE 284 C": (0, 102, 204),
    "PANTONE 2925 C": (0, 159, 227),
    "PANTONE 298 C": (0, 173, 239),
    "PANTONE 299 C": (0, 191, 243),
    "PANTONE 300 C": (0, 147, 221),
    "PANTONE Blue 072 C": (16, 24, 149),
    "PANTONE Reflex Blue C": (0, 20, 137),

    # Purples
    "PANTONE 267 C": (79, 38, 131),
    "PANTONE 268 C": (102, 45, 145),
    "PANTONE 2592 C": (101, 57, 168),
    "PANTONE 2593 C": (124, 81, 173),
    "PANTONE 2577 C": (95, 37, 159),
    "PANTONE 2583 C": (132, 85, 183),
    "PANTONE Violet C": (68, 0, 85),

    # Pinks
    "PANTONE 213 C": (255, 105, 180),
    "PANTONE 219 C": (236, 0, 140),
    "PANTONE 225 C": (255, 119, 193),
    "PANTONE 230 C": (228, 0, 127),
    "PANTONE Rhodamine Red C": (228, 0, 127),
    "PANTONE Pink C": (212, 191, 202),

    # Browns
    "PANTONE 168 C": (130, 56, 56),
    "PANTONE 4625 C": (109, 86, 70),
    "PANTONE 476 C": (130, 117, 107),
    "PANTONE 7518 C": (140, 98, 57),
    "PANTONE 7587 C": (148, 116, 64),

    # Grays
    "PANTONE Cool Gray 1 C": (216, 216, 214),
    "PANTONE Cool Gray 3 C": (197, 198, 196),
    "PANTONE Cool Gray 5 C": (177, 179, 179),
    "PANTONE Cool Gray 7 C": (151, 153, 155),
    "PANTONE Cool Gray 9 C": (117, 120, 123),
    "PANTONE Cool Gray 11 C": (83, 86, 90),
    "PANTONE Warm Gray 1 C": (213, 209, 203),
    "PANTONE Warm Gray 3 C": (196, 190, 182),
    "PANTONE Warm Gray 5 C": (179, 172, 162),
    "PANTONE Warm Gray 7 C": (153, 146, 137),
    "PANTONE Warm Gray 9 C": (121, 115, 107),
    "PANTONE Warm Gray 11 C": (82, 79, 73),

    # Black and White
    "PANTONE Black C": (45, 41, 38),
    "PANTONE Process Black C": (0, 0, 0),
    "PANTONE White": (255, 255, 255),

    # Additional popular colors
    "PANTONE 293 C": (0, 32, 91),
    "PANTONE 2728 C": (0, 40, 104),
    "PANTONE 7687 C": (42, 209, 201),
    "PANTONE 7688 C": (0, 181, 172),
    "PANTONE 7689 C": (0, 158, 150),
    "PANTONE 801 C": (0, 177, 172),
    "PANTONE 802 C": (99, 215, 210),
    "PANTONE Teal C": (0, 132, 137),
}


def calculate_color_distance(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """
    Calculate Euclidean distance between two RGB colors.

    Args:
        rgb1: First RGB color as (R, G, B) tuple
        rgb2: Second RGB color as (R, G, B) tuple

    Returns:
        Distance value (lower means more similar)
    """
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2

    # Euclidean distance in RGB space
    distance = math.sqrt((r2 - r1)**2 + (g2 - g1)**2 + (b2 - b1)**2)

    return distance


def rgb_to_pantone(r: int, g: int, b: int, top_n: int = 1) -> List[Tuple[str, Tuple[int, int, int], float]]:
    """
    Convert RGB color to closest Pantone color(s).

    Args:
        r: Red value (0-255)
        g: Green value (0-255)
        b: Blue value (0-255)
        top_n: Number of closest matches to return

    Returns:
        List of tuples containing (pantone_name, pantone_rgb, distance)
    """
    # Validate RGB values
    if not all(0 <= val <= 255 for val in [r, g, b]):
        raise ValueError("RGB values must be between 0 and 255")

    input_rgb = (r, g, b)

    # Calculate distances to all Pantone colors
    distances = []
    for pantone_name, pantone_rgb in PANTONE_COLORS.items():
        distance = calculate_color_distance(input_rgb, pantone_rgb)
        distances.append((pantone_name, pantone_rgb, distance))

    # Sort by distance (closest first)
    distances.sort(key=lambda x: x[2])

    return distances[:top_n]


def get_color_family(pantone_name: str) -> str:
    """
    Extract color family from Pantone name.

    Args:
        pantone_name: Full Pantone color name

    Returns:
        Color family name
    """
    pantone_lower = pantone_name.lower()

    if any(word in pantone_lower for word in ['red', '185', '186', '187', '1788', '1795', '1805']):
        return "Red Family"
    elif any(word in pantone_lower for word in ['orange', '021', '151', '158', '165', '1575', '1585']):
        return "Orange Family"
    elif any(word in pantone_lower for word in ['yellow', '100', '101', '102', '109', '116', '123']):
        return "Yellow Family"
    elif any(word in pantone_lower for word in ['green', '347', '348', '349', '354', '355', '356', '364', '375']):
        return "Green Family"
    elif any(word in pantone_lower for word in ['blue', '286', '285', '284', '2925', '298', '299', '300', '072', 'reflex', '293', '2728', 'teal', '801', '802']):
        return "Blue Family"
    elif any(word in pantone_lower for word in ['violet', 'purple', '267', '268', '2592', '2593', '2577', '2583']):
        return "Purple/Violet Family"
    elif any(word in pantone_lower for word in ['pink', 'rhodamine', '213', '219', '225', '230']):
        return "Pink Family"
    elif any(word in pantone_lower for word in ['brown', '168', '4625', '476', '7518', '7587']):
        return "Brown Family"
    elif 'gray' in pantone_lower or 'grey' in pantone_lower:
        return "Gray Family"
    elif 'black' in pantone_lower:
        return "Black Family"
    elif 'white' in pantone_lower:
        return "White Family"
    else:
        return "Other"


def format_rgb_display(rgb: Tuple[int, int, int]) -> str:
    """Format RGB tuple for display."""
    return f"RGB({rgb[0]}, {rgb[1]}, {rgb[2]})"


def print_color_match(rank: int, pantone_name: str, pantone_rgb: Tuple[int, int, int],
                      distance: float, input_rgb: Tuple[int, int, int]) -> None:
    """Print formatted color match information."""
    color_family = get_color_family(pantone_name)

    print(f"\n{'='*60}")
    if rank == 1:
        print(f"BEST MATCH:")
    else:
        print(f"MATCH #{rank}:")
    print(f"{'='*60}")
    print(f"Pantone Color:    {pantone_name}")
    print(f"Color Family:     {color_family}")
    print(f"Input RGB:        {format_rgb_display(input_rgb)}")
    print(f"Pantone RGB:      {format_rgb_display(pantone_rgb)}")
    print(f"Distance:         {distance:.2f}")

    # Calculate similarity percentage (inverse of distance, normalized)
    max_distance = math.sqrt(255**2 + 255**2 + 255**2)  # Maximum possible distance
    similarity = 100 * (1 - distance / max_distance)
    print(f"Similarity:       {similarity:.1f}%")


def main():
    """Main function for command-line interface."""
    parser = argparse.ArgumentParser(
        description='Convert RGB color codes to Pantone color families',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s 255 0 0                    # Convert pure red
  %(prog)s 100 150 200 --top 3        # Show top 3 matches
  %(prog)s 50 100 150 -t 5            # Show top 5 matches
        '''
    )

    parser.add_argument('r', type=int, help='Red value (0-255)')
    parser.add_argument('g', type=int, help='Green value (0-255)')
    parser.add_argument('b', type=int, help='Blue value (0-255)')
    parser.add_argument('-t', '--top', type=int, default=1,
                       help='Number of top matches to display (default: 1)')

    args = parser.parse_args()

    try:
        # Get Pantone matches
        matches = rgb_to_pantone(args.r, args.g, args.b, args.top)

        # Display header
        print("\n" + "="*60)
        print("RGB TO PANTONE CONVERTER")
        print("="*60)
        print(f"Input: {format_rgb_display((args.r, args.g, args.b))}")
        print(f"Finding top {args.top} Pantone match(es)...")

        # Display matches
        for i, (pantone_name, pantone_rgb, distance) in enumerate(matches, 1):
            print_color_match(i, pantone_name, pantone_rgb, distance, (args.r, args.g, args.b))

        print("\n" + "="*60 + "\n")

    except ValueError as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
