# RealityShift Motion and Transition Implementation Reference

This reference provides the mathematical formulations, algorithmic logic, easing functions, and implementation code for 2.5D camera dynamics and scene transitions in the RealityShift pipeline.

---

## 1. 2.5D Ken Burns Motion Mathematics

To transform static AI plates into cinematic vertical shots without introducing black borders, pixel shimmering, or motion sickness, the compositor applies parametric camera transforms.

### 1.1 Mathematical Formulation

Let:
- $W, H = 1080, 1920$ (Canvas dimensions).
- $W_{src}, H_{src}$ (Source image dimensions, where $W_{src} \ge 1440, H_{src} \ge 2560$).
- $t \in [0, d]$ (Current scene time, where $d$ is scene duration).
- $\tau = \frac{t}{d} \in [0.0, 1.0]$ (Normalized scene progress).
- $f(\tau)$ (Easing function mapping $[0, 1] \to [0, 1]$).

The instantaneous camera state at normalized time $\tau$ is defined by:
$$\text{Scale: } S(\tau) = S_{start} + (S_{end} - S_{start}) \cdot f(\tau)$$
$$\text{Center } X: C_x(\tau) = C_{x, start} + (C_{x, end} - C_{x, start}) \cdot f(\tau)$$
$$\text{Center } Y: C_y(\tau) = C_{y, start} + (C_{y, end} - C_{y, start}) \cdot f(\tau)$$
$$\text{Rotation: } \theta(\tau) = \theta_{start} + (\theta_{end} - \theta_{start}) \cdot f(\tau)$$

### 1.2 The Absolute No-Black-Border Guardrail
To guarantee that the camera window never exposes empty canvas voids or black margins:
$$S_{min} \ge 1.02 \times \max\left(\frac{W}{W_{src}}, \frac{H}{H_{src}}\right)$$
The pan coordinates must be clamped strictly such that:
$$C_x \in \left[\frac{W}{2 \cdot S}, W_{src} - \frac{W}{2 \cdot S}\right], \quad C_y \in \left[\frac{H}{2 \cdot S}, H_{src} - \frac{H}{2 \cdot S}\right]$$
If an image rotation $\theta \ne 0$ is applied, the minimum scale $S_{min}$ must be multiplied by an additional factor of:
$$S_{rot\_margin} = |\cos(\theta)| + |\sin(\theta)| \cdot \frac{H}{W}$$
*(For typical subtle rotations of $\pm 1.5^\circ$, an extra $3\%$ scale margin is sufficient).*

---

## 2. Easing Functions for Natural Physics

Linear interpolation ($\tau$) feels mechanical and robotic. Cinematic camera work requires smooth acceleration and deceleration curves:

```python
import math

def ease_in_out_cubic(tau: float) -> float:
    """Cubic Ease-In-Out: Smooth cinematic acceleration and deceleration."""
    tau = max(0.0, min(1.0, tau))
    if tau < 0.5:
        return 4.0 * tau * tau * tau
    else:
        return 1.0 - math.pow(-2.0 * tau + 2.0, 3) / 2.0

def ease_out_quad(tau: float) -> float:
    """Quadratic Ease-Out: Immediate impact that gently decelerates."""
    tau = max(0.0, min(1.0, tau))
    return 1.0 - (1.0 - tau) * (1.0 - tau)

def ease_in_sine(tau: float) -> float:
    """Sine Ease-In: Slow build-up into a dramatic reveal."""
    tau = max(0.0, min(1.0, tau))
    return 1.0 - math.cos((tau * math.pi) / 2.0)

def smoothstep(tau: float) -> float:
    """Classic Hermite Smoothstep: Zero 1st derivative at endpoints."""
    tau = max(0.0, min(1.0, tau))
    return tau * tau * (3.0 - 2.0 * tau)
```

---

## 3. Standard Camera Motion Archetypes

| Motion Archetype | $S_{start} \to S_{end}$ | Pan Movement | Easing Curve | Best Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Cosmic Push-In** | $1.04 \to 1.18$ | Center $\to$ Center | `ease_in_out_cubic` | Curiosity hooks, zooming into a mystery, black hole accretion disc. |
| **Cataclysmic Drift** | $1.15 \to 1.05$ | Pan Down ($C_y + 120\text{px}$) | `smoothstep` | Escalating disasters, collapsing atmospheres, tidal flooding. |
| **Astrophysics Sweep**| $1.08 \to 1.14$ | Pan Right ($C_x + 180\text{px}$) | `smoothstep` | Solar system orbits, stellar arrays, megastructure scale. |
| **Introspective Float**| $1.06 \to 1.09$ | Subtle drift + Roll ($\pm 0.8^\circ$) | `ease_in_out_cubic` | Climax realizations, philosophical reflections, closing CTA. |

---

## 4. Scene Transition Protocols

In high-retention YouTube Shorts, transitions must be fast, purposeful, and rhythmically aligned to audio cues. Slow crossfades destroy viewer retention.

### 4.1 Transition Specifications

| Transition Type | Duration ($s$) | Compositing Logic | Audio Sync Requirement |
| :--- | :--- | :--- | :--- |
| **Hard Cut** | $0.0\text{s}$ (Instant) | Frame $N$ is Scene A; Frame $N+1$ is Scene B. | Instant impact beat, silence cut, or punch SFX. |
| **Micro Cross-Dissolve** | $0.15\text{--}0.25\text{s}$ | Linear alpha blend: $\alpha_A = 1 - \tau_{trans}$, $\alpha_B = \tau_{trans}$. | Soft ambient sweep or continuous background pad. |
| **Whip Pan / Warp Blur** | $0.18\text{--}0.22\text{s}$ | Horizontal directional displacement with directional blur kernel. | High-frequency whoosh SFX peaking at the cut midpoint. |
| **Cosmic Glitch / Flash**| $0.10\text{--}0.14\text{s}$ | White flash frame with momentary RGB chromatic aberration shift. | Synthetic glitch click / bass drop. |

### 4.2 Audio-Visual Cut Synchronization
For transitions utilizing an audio whoosh or riser:
- The whoosh audio peak must align **exactly** with the visual cut boundary ($t_{cut}$).
- Pre-cut riser duration: $0.12\text{s}$ before $t_{cut}$.
- Post-cut decay duration: $0.08\text{s}$ after $t_{cut}$.
- Total audible SFX duration: $0.20\text{s}$.

```
Visual: [   SCENE A   ] [CUT] [   SCENE B   ]
Audio:        /---------\
SFX:     [Riser]       [Decay]
               ^ Peak at Cut
```

