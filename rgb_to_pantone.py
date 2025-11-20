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
# Comprehensive database covering all major Pantone color families
PANTONE_COLORS = {
    # ========== REDS ==========
    "PANTONE 179 C": (233, 124, 130),
    "PANTONE 180 C": (228, 113, 122),
    "PANTONE 181 C": (221, 103, 112),
    "PANTONE 184 C": (244, 51, 69),
    "PANTONE 185 C": (228, 0, 43),
    "PANTONE 186 C": (200, 16, 46),
    "PANTONE 187 C": (167, 25, 48),
    "PANTONE 1767 C": (255, 56, 71),
    "PANTONE 1775 C": (255, 38, 38),
    "PANTONE 1777 C": (239, 46, 36),
    "PANTONE 1785 C": (250, 39, 52),
    "PANTONE 1787 C": (246, 29, 54),
    "PANTONE 1788 C": (228, 0, 69),
    "PANTONE 1795 C": (228, 0, 127),
    "PANTONE 1797 C": (199, 0, 117),
    "PANTONE 1805 C": (228, 85, 133),
    "PANTONE 1807 C": (199, 71, 121),
    "PANTONE 1815 C": (239, 71, 111),
    "PANTONE 1817 C": (228, 61, 104),
    "PANTONE Red 032 C": (239, 51, 64),
    "PANTONE 192 C": (134, 38, 51),
    "PANTONE 193 C": (117, 40, 52),
    "PANTONE 194 C": (101, 45, 55),
    "PANTONE 195 C": (244, 101, 115),
    "PANTONE 196 C": (242, 71, 91),
    "PANTONE 197 C": (239, 46, 66),
    "PANTONE 198 C": (228, 0, 43),
    "PANTONE 199 C": (200, 16, 46),
    "PANTONE 200 C": (167, 25, 48),
    "PANTONE 201 C": (145, 31, 51),
    "PANTONE 202 C": (132, 36, 54),

    # ========== PINKS ==========
    "PANTONE 176 C": (255, 102, 153),
    "PANTONE 177 C": (255, 77, 136),
    "PANTONE 178 C": (250, 64, 129),
    "PANTONE 182 C": (244, 114, 139),
    "PANTONE 183 C": (247, 152, 175),
    "PANTONE 189 C": (204, 51, 102),
    "PANTONE 190 C": (176, 43, 88),
    "PANTONE 191 C": (153, 41, 78),
    "PANTONE 203 C": (255, 128, 168),
    "PANTONE 204 C": (255, 102, 153),
    "PANTONE 205 C": (250, 82, 144),
    "PANTONE 206 C": (246, 71, 140),
    "PANTONE 207 C": (242, 51, 132),
    "PANTONE 208 C": (228, 0, 127),
    "PANTONE 209 C": (199, 0, 117),
    "PANTONE 210 C": (255, 209, 220),
    "PANTONE 211 C": (255, 191, 208),
    "PANTONE 212 C": (255, 171, 197),
    "PANTONE 213 C": (255, 105, 180),
    "PANTONE 214 C": (250, 100, 173),
    "PANTONE 215 C": (242, 91, 170),
    "PANTONE 216 C": (228, 82, 163),
    "PANTONE 217 C": (255, 179, 206),
    "PANTONE 218 C": (255, 153, 194),
    "PANTONE 219 C": (236, 0, 140),
    "PANTONE 224 C": (255, 186, 212),
    "PANTONE 225 C": (255, 119, 193),
    "PANTONE 226 C": (255, 94, 184),
    "PANTONE 227 C": (250, 69, 177),
    "PANTONE 230 C": (228, 0, 127),
    "PANTONE 231 C": (196, 0, 112),
    "PANTONE 232 C": (173, 0, 99),
    "PANTONE Rhodamine Red C": (228, 0, 127),
    "PANTONE Pink C": (212, 191, 202),
    "PANTONE 236 C": (250, 100, 199),
    "PANTONE 237 C": (250, 77, 194),
    "PANTONE 238 C": (246, 56, 189),
    "PANTONE 239 C": (242, 0, 184),
    "PANTONE 240 C": (214, 0, 168),
    "PANTONE 241 C": (186, 12, 154),

    # ========== MAGENTAS ==========
    "PANTONE 233 C": (234, 179, 212),
    "PANTONE 234 C": (255, 140, 209),
    "PANTONE 246 C": (226, 96, 174),
    "PANTONE 247 C": (214, 81, 166),
    "PANTONE 248 C": (201, 71, 158),
    "PANTONE 249 C": (191, 0, 143),
    "PANTONE 250 C": (168, 0, 132),
    "PANTONE 251 C": (147, 0, 119),
    "PANTONE 2562 C": (255, 128, 204),
    "PANTONE 2563 C": (255, 102, 196),
    "PANTONE 2567 C": (250, 71, 189),
    "PANTONE 2572 C": (242, 51, 184),
    "PANTONE 2573 C": (228, 35, 176),
    "PANTONE 2577 C": (95, 37, 159),

    # ========== PURPLES & VIOLETS ==========
    "PANTONE 252 C": (186, 152, 197),
    "PANTONE 253 C": (175, 136, 188),
    "PANTONE 254 C": (163, 120, 179),
    "PANTONE 255 C": (145, 96, 166),
    "PANTONE 256 C": (132, 85, 158),
    "PANTONE 257 C": (119, 73, 150),
    "PANTONE 258 C": (107, 61, 143),
    "PANTONE 259 C": (212, 175, 212),
    "PANTONE 260 C": (196, 157, 201),
    "PANTONE 261 C": (181, 141, 191),
    "PANTONE 262 C": (153, 102, 173),
    "PANTONE 263 C": (142, 91, 166),
    "PANTONE 264 C": (130, 81, 158),
    "PANTONE 265 C": (119, 71, 150),
    "PANTONE 266 C": (107, 61, 143),
    "PANTONE 267 C": (79, 38, 131),
    "PANTONE 268 C": (102, 45, 145),
    "PANTONE 269 C": (91, 35, 137),
    "PANTONE 2562 C": (255, 128, 204),
    "PANTONE 2567 C": (250, 71, 189),
    "PANTONE 2572 C": (242, 51, 184),
    "PANTONE 2582 C": (163, 130, 199),
    "PANTONE 2583 C": (132, 85, 183),
    "PANTONE 2592 C": (101, 57, 168),
    "PANTONE 2593 C": (124, 81, 173),
    "PANTONE 2602 C": (140, 91, 186),
    "PANTONE 2603 C": (132, 85, 181),
    "PANTONE 2612 C": (173, 145, 201),
    "PANTONE 2613 C": (163, 135, 194),
    "PANTONE 2622 C": (153, 117, 188),
    "PANTONE 2623 C": (145, 109, 181),
    "PANTONE 2627 C": (163, 130, 199),
    "PANTONE 2628 C": (153, 119, 191),
    "PANTONE 2685 C": (102, 51, 153),
    "PANTONE 2695 C": (89, 43, 143),
    "PANTONE Violet C": (68, 0, 85),
    "PANTONE Purple C": (194, 86, 199),
    "PANTONE 270 C": (189, 153, 201),
    "PANTONE 271 C": (175, 136, 191),
    "PANTONE 272 C": (163, 119, 181),

    # ========== BLUES ==========
    "PANTONE 278 C": (173, 181, 214),
    "PANTONE 279 C": (153, 168, 209),
    "PANTONE 280 C": (130, 153, 204),
    "PANTONE 281 C": (89, 119, 186),
    "PANTONE 282 C": (71, 102, 173),
    "PANTONE 283 C": (56, 87, 163),
    "PANTONE 284 C": (0, 102, 204),
    "PANTONE 285 C": (0, 57, 166),
    "PANTONE 286 C": (0, 45, 114),
    "PANTONE 287 C": (0, 40, 104),
    "PANTONE 288 C": (0, 35, 95),
    "PANTONE 289 C": (0, 30, 85),
    "PANTONE 290 C": (191, 204, 228),
    "PANTONE 291 C": (163, 186, 219),
    "PANTONE 292 C": (107, 145, 204),
    "PANTONE 293 C": (0, 32, 91),
    "PANTONE 294 C": (0, 107, 186),
    "PANTONE 295 C": (0, 94, 173),
    "PANTONE 296 C": (0, 84, 163),
    "PANTONE 297 C": (130, 204, 242),
    "PANTONE 298 C": (0, 173, 239),
    "PANTONE 299 C": (0, 191, 243),
    "PANTONE 300 C": (0, 147, 221),
    "PANTONE 301 C": (0, 137, 207),
    "PANTONE 302 C": (0, 124, 194),
    "PANTONE 303 C": (0, 114, 186),
    "PANTONE 304 C": (163, 214, 245),
    "PANTONE 305 C": (140, 204, 242),
    "PANTONE 306 C": (0, 181, 226),
    "PANTONE 2706 C": (117, 170, 219),
    "PANTONE 2707 C": (107, 163, 214),
    "PANTONE 2708 C": (0, 91, 187),
    "PANTONE 2718 C": (0, 107, 206),
    "PANTONE 2728 C": (0, 40, 104),
    "PANTONE 2738 C": (0, 48, 135),
    "PANTONE 2748 C": (0, 56, 168),
    "PANTONE 2758 C": (0, 66, 194),
    "PANTONE 2905 C": (0, 151, 212),
    "PANTONE 2915 C": (0, 140, 201),
    "PANTONE 2925 C": (0, 159, 227),
    "PANTONE 2935 C": (0, 151, 219),
    "PANTONE 2945 C": (0, 143, 209),
    "PANTONE Blue 072 C": (16, 24, 149),
    "PANTONE Reflex Blue C": (0, 20, 137),
    "PANTONE Process Blue C": (0, 133, 202),

    # ========== TEALS & AQUAS ==========
    "PANTONE 310 C": (0, 147, 178),
    "PANTONE 311 C": (0, 137, 169),
    "PANTONE 312 C": (0, 126, 163),
    "PANTONE 313 C": (168, 223, 233),
    "PANTONE 314 C": (153, 217, 228),
    "PANTONE 315 C": (0, 179, 201),
    "PANTONE 316 C": (0, 168, 194),
    "PANTONE 317 C": (140, 209, 219),
    "PANTONE 318 C": (0, 188, 209),
    "PANTONE 319 C": (0, 175, 199),
    "PANTONE 320 C": (0, 158, 186),
    "PANTONE 321 C": (0, 145, 178),
    "PANTONE 322 C": (0, 132, 168),
    "PANTONE 323 C": (130, 207, 214),
    "PANTONE 324 C": (107, 196, 204),
    "PANTONE 325 C": (64, 183, 196),
    "PANTONE 326 C": (0, 168, 184),
    "PANTONE 327 C": (0, 153, 173),
    "PANTONE Teal C": (0, 132, 137),
    "PANTONE 328 C": (0, 130, 153),
    "PANTONE 329 C": (0, 119, 145),
    "PANTONE 330 C": (0, 107, 135),
    "PANTONE 7466 C": (0, 125, 152),
    "PANTONE 7467 C": (0, 115, 143),
    "PANTONE 7468 C": (0, 104, 133),
    "PANTONE 7469 C": (0, 94, 122),
    "PANTONE 7470 C": (0, 84, 112),
    "PANTONE 7471 C": (0, 74, 102),
    "PANTONE 7687 C": (42, 209, 201),
    "PANTONE 7688 C": (0, 181, 172),
    "PANTONE 7689 C": (0, 158, 150),
    "PANTONE 801 C": (0, 177, 172),
    "PANTONE 802 C": (99, 215, 210),
    "PANTONE 803 C": (168, 232, 227),

    # ========== GREENS ==========
    "PANTONE 331 C": (186, 216, 10),
    "PANTONE 332 C": (168, 205, 0),
    "PANTONE 333 C": (0, 122, 83),
    "PANTONE 334 C": (0, 112, 74),
    "PANTONE 335 C": (0, 102, 65),
    "PANTONE 336 C": (0, 92, 58),
    "PANTONE 337 C": (0, 163, 104),
    "PANTONE 338 C": (0, 153, 96),
    "PANTONE 339 C": (0, 143, 88),
    "PANTONE 340 C": (0, 168, 119),
    "PANTONE 341 C": (0, 158, 109),
    "PANTONE 342 C": (0, 148, 101),
    "PANTONE 343 C": (0, 138, 91),
    "PANTONE 344 C": (168, 214, 117),
    "PANTONE 345 C": (145, 204, 96),
    "PANTONE 346 C": (122, 194, 68),
    "PANTONE 347 C": (0, 143, 81),
    "PANTONE 348 C": (0, 135, 68),
    "PANTONE 349 C": (0, 119, 73),
    "PANTONE 350 C": (0, 107, 66),
    "PANTONE 351 C": (212, 232, 150),
    "PANTONE 352 C": (196, 226, 130),
    "PANTONE 353 C": (181, 219, 109),
    "PANTONE 354 C": (0, 175, 102),
    "PANTONE 355 C": (0, 158, 96),
    "PANTONE 356 C": (0, 142, 91),
    "PANTONE 357 C": (0, 130, 82),
    "PANTONE 358 C": (181, 214, 137),
    "PANTONE 359 C": (168, 209, 122),
    "PANTONE 360 C": (153, 204, 102),
    "PANTONE 361 C": (122, 184, 0),
    "PANTONE 362 C": (107, 168, 0),
    "PANTONE 363 C": (94, 153, 0),
    "PANTONE 364 C": (103, 194, 58),
    "PANTONE 365 C": (84, 181, 38),
    "PANTONE 366 C": (69, 168, 22),
    "PANTONE 367 C": (58, 153, 9),
    "PANTONE 368 C": (130, 191, 0),
    "PANTONE 369 C": (117, 181, 0),
    "PANTONE 370 C": (107, 168, 0),
    "PANTONE 371 C": (94, 153, 0),
    "PANTONE 372 C": (181, 214, 51),
    "PANTONE 373 C": (168, 204, 38),
    "PANTONE 374 C": (153, 191, 26),
    "PANTONE 375 C": (139, 198, 63),
    "PANTONE 376 C": (122, 184, 0),
    "PANTONE 377 C": (107, 168, 0),
    "PANTONE 378 C": (94, 153, 0),
    "PANTONE Green C": (0, 173, 131),

    # ========== YELLOWS & GOLDS ==========
    "PANTONE 100 C": (244, 237, 98),
    "PANTONE 101 C": (244, 237, 71),
    "PANTONE 102 C": (254, 228, 64),
    "PANTONE 103 C": (255, 225, 43),
    "PANTONE 104 C": (255, 219, 28),
    "PANTONE 105 C": (255, 214, 10),
    "PANTONE 106 C": (255, 209, 0),
    "PANTONE 107 C": (250, 237, 137),
    "PANTONE 108 C": (250, 232, 117),
    "PANTONE 109 C": (255, 214, 0),
    "PANTONE 110 C": (250, 209, 0),
    "PANTONE 111 C": (244, 202, 0),
    "PANTONE 112 C": (237, 194, 0),
    "PANTONE 113 C": (232, 186, 0),
    "PANTONE 114 C": (255, 214, 79),
    "PANTONE 115 C": (255, 209, 56),
    "PANTONE 116 C": (255, 200, 8),
    "PANTONE 117 C": (255, 196, 37),
    "PANTONE 118 C": (255, 188, 28),
    "PANTONE 119 C": (255, 181, 18),
    "PANTONE 120 C": (250, 173, 10),
    "PANTONE 121 C": (255, 204, 102),
    "PANTONE 122 C": (255, 196, 84),
    "PANTONE 123 C": (255, 188, 0),
    "PANTONE 124 C": (255, 181, 18),
    "PANTONE 125 C": (250, 173, 26),
    "PANTONE 126 C": (244, 168, 28),
    "PANTONE 127 C": (237, 163, 26),
    "PANTONE Yellow C": (254, 221, 0),
    "PANTONE Yellow 012 C": (254, 221, 0),
    "PANTONE 128 C": (242, 169, 0),
    "PANTONE 129 C": (239, 163, 0),
    "PANTONE 130 C": (232, 155, 0),
    "PANTONE 131 C": (226, 150, 0),
    "PANTONE 132 C": (219, 145, 0),
    "PANTONE 133 C": (214, 140, 0),
    "PANTONE 134 C": (209, 135, 0),

    # ========== ORANGES ==========
    "PANTONE 135 C": (255, 168, 51),
    "PANTONE 136 C": (255, 163, 38),
    "PANTONE 137 C": (255, 158, 28),
    "PANTONE 138 C": (255, 153, 18),
    "PANTONE 139 C": (255, 145, 10),
    "PANTONE 140 C": (255, 140, 0),
    "PANTONE 141 C": (250, 135, 0),
    "PANTONE 142 C": (255, 145, 48),
    "PANTONE 143 C": (255, 140, 38),
    "PANTONE 144 C": (255, 135, 28),
    "PANTONE 145 C": (255, 130, 18),
    "PANTONE 146 C": (255, 122, 10),
    "PANTONE 147 C": (250, 117, 0),
    "PANTONE 148 C": (244, 112, 0),
    "PANTONE 149 C": (255, 122, 33),
    "PANTONE 150 C": (255, 117, 24),
    "PANTONE 151 C": (255, 104, 31),
    "PANTONE 152 C": (255, 109, 20),
    "PANTONE 153 C": (255, 102, 13),
    "PANTONE 154 C": (250, 99, 3),
    "PANTONE 155 C": (244, 94, 0),
    "PANTONE 156 C": (255, 109, 28),
    "PANTONE 157 C": (255, 102, 18),
    "PANTONE 158 C": (255, 103, 31),
    "PANTONE 159 C": (255, 94, 10),
    "PANTONE 160 C": (250, 89, 0),
    "PANTONE 161 C": (244, 84, 0),
    "PANTONE 162 C": (237, 79, 0),
    "PANTONE 163 C": (255, 102, 18),
    "PANTONE 164 C": (255, 94, 10),
    "PANTONE 165 C": (255, 94, 0),
    "PANTONE 166 C": (250, 89, 0),
    "PANTONE 167 C": (244, 84, 0),
    "PANTONE 168 C": (130, 56, 56),
    "PANTONE 169 C": (122, 51, 51),
    "PANTONE 021 C": (254, 80, 0),
    "PANTONE 1575 C": (255, 109, 0),
    "PANTONE 1585 C": (255, 99, 25),
    "PANTONE 1595 C": (255, 89, 10),
    "PANTONE 1605 C": (250, 84, 0),
    "PANTONE 1615 C": (244, 79, 0),
    "PANTONE 1625 C": (237, 74, 0),
    "PANTONE Orange 021 C": (254, 80, 0),

    # ========== BROWNS & TANS ==========
    "PANTONE 4625 C": (109, 86, 70),
    "PANTONE 4635 C": (99, 76, 61),
    "PANTONE 4645 C": (89, 68, 54),
    "PANTONE 4655 C": (79, 58, 47),
    "PANTONE 4665 C": (69, 50, 40),
    "PANTONE 4675 C": (61, 43, 35),
    "PANTONE 4685 C": (53, 37, 30),
    "PANTONE 462 C": (196, 181, 163),
    "PANTONE 463 C": (186, 168, 147),
    "PANTONE 464 C": (175, 155, 130),
    "PANTONE 465 C": (163, 142, 117),
    "PANTONE 466 C": (153, 130, 102),
    "PANTONE 467 C": (140, 117, 89),
    "PANTONE 468 C": (130, 107, 79),
    "PANTONE 469 C": (196, 175, 150),
    "PANTONE 470 C": (186, 163, 135),
    "PANTONE 471 C": (175, 150, 120),
    "PANTONE 472 C": (163, 137, 107),
    "PANTONE 473 C": (153, 124, 94),
    "PANTONE 474 C": (140, 112, 84),
    "PANTONE 475 C": (130, 102, 74),
    "PANTONE 476 C": (130, 117, 107),
    "PANTONE 477 C": (122, 107, 96),
    "PANTONE 478 C": (112, 96, 84),
    "PANTONE 479 C": (102, 86, 73),
    "PANTONE 480 C": (91, 76, 63),
    "PANTONE 481 C": (81, 66, 54),
    "PANTONE 482 C": (71, 56, 46),
    "PANTONE 7499 C": (181, 145, 117),
    "PANTONE 7500 C": (168, 130, 102),
    "PANTONE 7501 C": (153, 117, 89),
    "PANTONE 7502 C": (140, 102, 76),
    "PANTONE 7503 C": (124, 89, 64),
    "PANTONE 7504 C": (112, 79, 56),
    "PANTONE 7505 C": (99, 69, 48),
    "PANTONE 7506 C": (196, 168, 140),
    "PANTONE 7507 C": (181, 150, 119),
    "PANTONE 7508 C": (168, 135, 102),
    "PANTONE 7509 C": (153, 119, 84),
    "PANTONE 7510 C": (140, 107, 71),
    "PANTONE 7511 C": (124, 91, 58),
    "PANTONE 7512 C": (112, 81, 51),
    "PANTONE 7513 C": (209, 181, 153),
    "PANTONE 7514 C": (196, 163, 135),
    "PANTONE 7515 C": (181, 145, 112),
    "PANTONE 7516 C": (168, 130, 94),
    "PANTONE 7517 C": (153, 114, 79),
    "PANTONE 7518 C": (140, 98, 57),
    "PANTONE 7519 C": (124, 84, 43),
    "PANTONE 7520 C": (214, 188, 163),
    "PANTONE 7521 C": (201, 173, 145),
    "PANTONE 7522 C": (186, 155, 124),
    "PANTONE 7523 C": (173, 140, 107),
    "PANTONE 7524 C": (158, 122, 89),
    "PANTONE 7525 C": (145, 107, 74),
    "PANTONE 7526 C": (130, 94, 61),
    "PANTONE 7527 C": (237, 214, 186),
    "PANTONE 7528 C": (226, 198, 168),
    "PANTONE 7529 C": (214, 181, 147),
    "PANTONE 7530 C": (201, 163, 130),
    "PANTONE 7531 C": (186, 145, 109),
    "PANTONE 7532 C": (173, 130, 91),
    "PANTONE 7533 C": (158, 112, 71),
    "PANTONE 7534 C": (242, 221, 196),
    "PANTONE 7535 C": (232, 207, 179),
    "PANTONE 7536 C": (221, 191, 158),
    "PANTONE 7537 C": (209, 175, 140),
    "PANTONE 7538 C": (196, 158, 119),
    "PANTONE 7539 C": (181, 140, 99),
    "PANTONE 7540 C": (168, 124, 79),
    "PANTONE 7586 C": (168, 140, 91),
    "PANTONE 7587 C": (148, 116, 64),

    # ========== GRAYS ==========
    "PANTONE Cool Gray 1 C": (216, 216, 214),
    "PANTONE Cool Gray 2 C": (206, 207, 206),
    "PANTONE Cool Gray 3 C": (197, 198, 196),
    "PANTONE Cool Gray 4 C": (186, 188, 186),
    "PANTONE Cool Gray 5 C": (177, 179, 179),
    "PANTONE Cool Gray 6 C": (166, 168, 170),
    "PANTONE Cool Gray 7 C": (151, 153, 155),
    "PANTONE Cool Gray 8 C": (135, 138, 143),
    "PANTONE Cool Gray 9 C": (117, 120, 123),
    "PANTONE Cool Gray 10 C": (99, 102, 106),
    "PANTONE Cool Gray 11 C": (83, 86, 90),
    "PANTONE Warm Gray 1 C": (213, 209, 203),
    "PANTONE Warm Gray 2 C": (204, 199, 191),
    "PANTONE Warm Gray 3 C": (196, 190, 182),
    "PANTONE Warm Gray 4 C": (186, 181, 172),
    "PANTONE Warm Gray 5 C": (179, 172, 162),
    "PANTONE Warm Gray 6 C": (168, 162, 153),
    "PANTONE Warm Gray 7 C": (153, 146, 137),
    "PANTONE Warm Gray 8 C": (140, 133, 125),
    "PANTONE Warm Gray 9 C": (121, 115, 107),
    "PANTONE Warm Gray 10 C": (107, 102, 93),
    "PANTONE Warm Gray 11 C": (82, 79, 73),
    "PANTONE Black 2 C": (61, 57, 53),
    "PANTONE Black 3 C": (48, 45, 41),
    "PANTONE Black 4 C": (40, 38, 35),
    "PANTONE Black 5 C": (35, 33, 30),
    "PANTONE Black 6 C": (28, 27, 25),
    "PANTONE Black 7 C": (20, 20, 18),

    # ========== BLACKS & WHITES ==========
    "PANTONE Black C": (45, 41, 38),
    "PANTONE Process Black C": (0, 0, 0),
    "PANTONE White": (255, 255, 255),

    # ========== METALLICS ==========
    "PANTONE 871 C": (135, 99, 0),
    "PANTONE 872 C": (150, 113, 0),
    "PANTONE 873 C": (168, 130, 0),
    "PANTONE 874 C": (186, 148, 38),
    "PANTONE 875 C": (194, 158, 61),
    "PANTONE 876 C": (204, 168, 84),
    "PANTONE 877 C": (153, 153, 153),

    # ========== NEONS & FLUORESCENTS ==========
    "PANTONE 801 C": (0, 177, 172),
    "PANTONE 802 C": (99, 215, 210),
    "PANTONE 803 C": (168, 232, 227),
    "PANTONE 804 C": (255, 242, 0),
    "PANTONE 805 C": (255, 247, 153),
    "PANTONE 806 C": (255, 105, 180),
    "PANTONE 807 C": (255, 170, 204),
    "PANTONE 808 C": (255, 20, 147),

    # ========== PASTELS ==========
    "PANTONE 9060 C": (242, 223, 227),
    "PANTONE 9061 C": (232, 204, 212),
    "PANTONE 9062 C": (221, 186, 196),
    "PANTONE 9063 C": (212, 168, 181),
    "PANTONE 9064 C": (201, 150, 168),
    "PANTONE 9065 C": (191, 130, 153),
    "PANTONE 9080 C": (232, 214, 221),
    "PANTONE 9081 C": (221, 196, 209),
    "PANTONE 9082 C": (209, 179, 196),
    "PANTONE 9100 C": (242, 237, 214),
    "PANTONE 9101 C": (237, 232, 196),
    "PANTONE 9102 C": (232, 226, 181),
    "PANTONE 9120 C": (237, 247, 232),
    "PANTONE 9121 C": (226, 242, 219),
    "PANTONE 9122 C": (214, 237, 204),
    "PANTONE 9140 C": (232, 247, 242),
    "PANTONE 9141 C": (219, 242, 237),
    "PANTONE 9142 C": (204, 237, 232),
    "PANTONE 9160 C": (232, 242, 247),
    "PANTONE 9161 C": (219, 237, 242),
    "PANTONE 9162 C": (204, 232, 242),

    # ========== EARTH TONES ==========
    "PANTONE 7548 C": (186, 140, 99),
    "PANTONE 7549 C": (173, 124, 79),
    "PANTONE 7550 C": (158, 107, 61),
    "PANTONE 7551 C": (145, 94, 48),
    "PANTONE 7552 C": (130, 79, 33),
    "PANTONE 7553 C": (117, 68, 23),
    "PANTONE 7554 C": (102, 56, 10),
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

    # Check for specific named colors first
    if 'white' in pantone_lower:
        return "White Family"
    elif 'black' in pantone_lower:
        return "Black Family"
    elif 'gray' in pantone_lower or 'grey' in pantone_lower:
        return "Gray Family"

    # Metallics
    elif any(word in pantone_lower for word in ['871', '872', '873', '874', '875', '876', '877']):
        return "Metallic Family"

    # Neons & Fluorescents
    elif any(word in pantone_lower for word in ['804', '805', '806', '807', '808']):
        return "Neon/Fluorescent Family"

    # Pastels
    elif pantone_lower.startswith('pantone 90') or pantone_lower.startswith('pantone 91'):
        return "Pastel Family"

    # Reds - comprehensive red family patterns
    elif any(word in pantone_lower for word in ['red']):
        return "Red Family"
    elif pantone_lower.startswith('pantone 1') and any(code in pantone_lower for code in
        ['179', '180', '181', '184', '185', '186', '187', '1767', '1775', '1777',
         '1785', '1787', '1788', '1795', '1797', '1805', '1807', '1815', '1817',
         '192', '193', '194', '195', '196', '197', '198', '199']):
        return "Red Family"
    elif pantone_lower.startswith('pantone 20') and any(code in pantone_lower for code in
        ['200', '201', '202']):
        return "Red Family"

    # Pinks
    elif 'pink' in pantone_lower or 'rhodamine' in pantone_lower:
        return "Pink Family"
    elif any(code in pantone_lower for code in
        ['176', '177', '178', '182', '183', '189', '190', '191',
         '203', '204', '205', '206', '207', '208', '209',
         '210', '211', '212', '213', '214', '215', '216', '217', '218', '219',
         '224', '225', '226', '227', '230', '231', '232']):
        return "Pink Family"

    # Magentas
    elif any(code in pantone_lower for code in
        ['233', '234', '236', '237', '238', '239', '240', '241',
         '246', '247', '248', '249', '250', '251']):
        return "Magenta Family"

    # Purples & Violets
    elif 'purple' in pantone_lower or 'violet' in pantone_lower:
        return "Purple/Violet Family"
    elif any(code in pantone_lower for code in
        ['252', '253', '254', '255', '256', '257', '258', '259',
         '260', '261', '262', '263', '264', '265', '266', '267', '268', '269',
         '270', '271', '272',
         '2562', '2563', '2567', '2572', '2573', '2577',
         '2582', '2583', '2592', '2593',
         '2602', '2603', '2612', '2613', '2622', '2623', '2627', '2628',
         '2685', '2695']):
        return "Purple/Violet Family"

    # Blues - comprehensive blue patterns
    elif 'blue' in pantone_lower:
        return "Blue Family"
    elif any(code in pantone_lower for code in
        ['278', '279', '280', '281', '282', '283', '284', '285', '286', '287', '288', '289',
         '290', '291', '292', '293', '294', '295', '296', '297', '298', '299',
         '300', '301', '302', '303', '304', '305', '306',
         '2706', '2707', '2708', '2718', '2728', '2738', '2748', '2758',
         '2905', '2915', '2925', '2935', '2945']):
        return "Blue Family"

    # Teals & Aquas
    elif 'teal' in pantone_lower:
        return "Teal/Aqua Family"
    elif any(code in pantone_lower for code in
        ['310', '311', '312', '313', '314', '315', '316', '317', '318', '319',
         '320', '321', '322', '323', '324', '325', '326', '327', '328', '329', '330',
         '7466', '7467', '7468', '7469', '7470', '7471',
         '7687', '7688', '7689',
         '801', '802', '803']):
        return "Teal/Aqua Family"

    # Greens - comprehensive green patterns
    elif 'green' in pantone_lower:
        return "Green Family"
    elif any(code in pantone_lower for code in
        ['331', '332', '333', '334', '335', '336', '337', '338', '339',
         '340', '341', '342', '343', '344', '345', '346', '347', '348', '349', '350',
         '351', '352', '353', '354', '355', '356', '357', '358', '359', '360',
         '361', '362', '363', '364', '365', '366', '367', '368', '369', '370',
         '371', '372', '373', '374', '375', '376', '377', '378']):
        return "Green Family"

    # Yellows & Golds
    elif 'yellow' in pantone_lower:
        return "Yellow Family"
    elif any(code in pantone_lower for code in
        ['100', '101', '102', '103', '104', '105', '106', '107', '108', '109',
         '110', '111', '112', '113', '114', '115', '116', '117', '118', '119',
         '120', '121', '122', '123', '124', '125', '126', '127', '128', '129',
         '130', '131', '132', '133', '134']):
        return "Yellow Family"

    # Oranges
    elif 'orange' in pantone_lower:
        return "Orange Family"
    elif any(code in pantone_lower for code in
        ['021', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145',
         '146', '147', '148', '149', '150', '151', '152', '153', '154', '155', '156', '157',
         '158', '159', '160', '161', '162', '163', '164', '165', '166', '167', '168', '169',
         '1575', '1585', '1595', '1605', '1615', '1625']):
        return "Orange Family"

    # Browns & Tans - comprehensive brown patterns
    elif 'brown' in pantone_lower:
        return "Brown/Tan Family"
    elif any(code in pantone_lower for code in
        ['462', '463', '464', '465', '466', '467', '468',
         '469', '470', '471', '472', '473', '474', '475',
         '476', '477', '478', '479', '480', '481', '482',
         '4625', '4635', '4645', '4655', '4665', '4675', '4685',
         '7499', '7500', '7501', '7502', '7503', '7504', '7505',
         '7506', '7507', '7508', '7509', '7510', '7511', '7512',
         '7513', '7514', '7515', '7516', '7517', '7518', '7519',
         '7520', '7521', '7522', '7523', '7524', '7525', '7526',
         '7527', '7528', '7529', '7530', '7531', '7532', '7533',
         '7534', '7535', '7536', '7537', '7538', '7539', '7540',
         '7548', '7549', '7550', '7551', '7552', '7553', '7554',
         '7586', '7587']):
        return "Brown/Tan Family"

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
