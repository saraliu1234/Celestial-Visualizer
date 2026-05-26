"""
utils.py — shared helper functions for the star-explosion visualizer.
"""

import numpy as np
import pygame

# Cache for radial gradient surfaces keyed by (radius, tuple_of_stops)
_gradient_cache: dict = {}


def make_radial_gradient(radius: int, stops: list) -> pygame.Surface:
    """
    Build a radial-gradient pygame Surface (SRCALPHA, size radius*2 × radius*2).

    Parameters
    ----------
    radius : int
        Half-size of the returned surface.
    stops : list of (t, (r, g, b, a))
        Colour stops where t ∈ [0, 1].

    Returns
    -------
    pygame.Surface  (SRCALPHA)
    """
    cache_key = (radius, tuple((t, c) for t, c in stops))
    if cache_key in _gradient_cache:
        return _gradient_cache[cache_key]

    size = radius * 2
    # Pixel-centre grid: both axes run from -radius to +radius
    # numpy uses (row, col) = (y, x), pygame surfarray uses (x, y) = (col, row)
    y_idx, x_idx = np.mgrid[-radius:radius, -radius:radius]  # shape (size, size)
    dist = np.sqrt(x_idx.astype(np.float32) ** 2 + y_idx.astype(np.float32) ** 2)
    t_arr = np.clip(dist / radius, 0.0, 1.0)  # normalised [0,1], shape (H, W)

    stop_ts = np.array([s[0] for s in stops], dtype=np.float32)
    stop_r = np.array([s[1][0] for s in stops], dtype=np.float32)
    stop_g = np.array([s[1][1] for s in stops], dtype=np.float32)
    stop_b = np.array([s[1][2] for s in stops], dtype=np.float32)
    stop_a = np.array([s[1][3] for s in stops], dtype=np.float32)

    ch_r = np.interp(t_arr, stop_ts, stop_r).astype(np.uint8)
    ch_g = np.interp(t_arr, stop_ts, stop_g).astype(np.uint8)
    ch_b = np.interp(t_arr, stop_ts, stop_b).astype(np.uint8)
    ch_a = np.interp(t_arr, stop_ts, stop_a).astype(np.uint8)

    # Stack into (H, W, 4), then transpose to (W, H, 4) for pygame surfarray
    rgba_hw = np.stack([ch_r, ch_g, ch_b, ch_a], axis=2)  # (H, W, 4)
    rgba_wh = rgba_hw.transpose(1, 0, 2)                   # (W, H, 4)

    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.surfarray.blit_array(surf, rgba_wh[:, :, :3])
    pxa = pygame.surfarray.pixels_alpha(surf)
    pxa[:] = rgba_wh[:, :, 3]
    del pxa  # release the lock

    _gradient_cache[cache_key] = surf
    return surf
