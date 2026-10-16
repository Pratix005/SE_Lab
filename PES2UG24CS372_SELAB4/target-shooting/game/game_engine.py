"""
GameEngine: owns the targets and handles player clicks.

The game has a 30-second round. During the round, targets move and
the player can shoot them. When the timer reaches zero, gameplay stops
and the final result is displayed until the player restarts the round.
"""

import random
import time

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28
BASE_POINTS = 10
ROUND_DURATION = 30


class GameEngine:
    def __init__(self):
        self._start_round()

    def _start_round(self):
        """Initialize or reset everything for a new round."""
        self.targets = [
            self._random_target(i) for i in range(NUM_TARGETS)
        ]

        self.hits = 0
        self.misses = 0

        self.score = 0
        self.combo = 1

        self.round_start_time = time.monotonic()
        self.round_over = False

    def restart_round(self):
        """Start a completely new 30-second round."""
        self._start_round()

    def _random_target(self, index=0):
        x = random.randint(
            TARGET_RADIUS + 10,
            WIDTH - TARGET_RADIUS - 10
        )
        y = random.randint(
            TARGET_RADIUS + 10,
            HEIGHT - TARGET_RADIUS - 10
        )

        # Different movement patterns/speeds for different targets.
        movement_patterns = [
            (2, 0),      # Slow horizontal movement
            (-3, 0),     # Faster horizontal movement
            (2, 2),      # Diagonal movement
        ]

        velocity_x, velocity_y = movement_patterns[
            index % len(movement_patterns)
        ]

        return Target(
            x,
            y,
            radius=TARGET_RADIUS,
            velocity_x=velocity_x,
            velocity_y=velocity_y
        )

    def get_remaining_time(self):
        """Return the number of whole seconds remaining."""
        if self.round_over:
            return 0

        elapsed = time.monotonic() - self.round_start_time
        remaining = ROUND_DURATION - elapsed

        return max(0, int(remaining + 0.999))

    def handle_click(self, pos):
        """Handle a player click only while the round is active."""
        if self.round_over:
            return

        target = check_hit(self.targets, pos)

        if target is not None:
            self.hits += 1

            # Award points using the current combo multiplier.
            self.score += BASE_POINTS * self.combo

            # Increase the multiplier for the next consecutive hit.
            self.combo += 1

            self.targets.remove(target)
            self.targets.append(
                self._random_target(len(self.targets))
            )
        else:
            self.misses += 1

            # A miss breaks the streak.
            self.combo = 1

    def update(self):
        """Update the game state while the round is active."""
        if self.round_over:
            return

        if time.monotonic() - self.round_start_time >= ROUND_DURATION:
            self.round_over = True
            return

        for target in self.targets:
            target.update(WIDTH, HEIGHT)

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.targets)

        remaining_time = self.get_remaining_time()

        renderer.draw_text(
            surface,
            font,
            (
                f"Time: {remaining_time}  "
                f"Score: {self.score}  "
                f"Combo: x{self.combo}"
            ),
            (10, 10)
        )

        if self.round_over:
            renderer.draw_banner(
                surface,
                font,
                f"ROUND OVER - Final Score: {self.score} - Press R to Restart"
            )
