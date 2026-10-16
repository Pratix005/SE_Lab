"""
Target: a circular target the player clicks on. (x, y) is the CENTER
of the circle - this matters for how it's drawn vs. how it's hit-tested.
"""

import pygame


class Target:
    def __init__(self, x, y, radius=28, color=(230, 90, 70),
                 velocity_x=0, velocity_y=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def update(self, width, height):
        """Move the target and bounce off the screen boundaries."""
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce horizontally while keeping the target fully on screen.
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.velocity_x = abs(self.velocity_x)
        elif self.x + self.radius >= width:
            self.x = width - self.radius
            self.velocity_x = -abs(self.velocity_x)

        # Bounce vertically while keeping the target fully on screen.
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.velocity_y = abs(self.velocity_y)
        elif self.y + self.radius >= height:
            self.y = height - self.radius
            self.velocity_y = -abs(self.velocity_y)

    def get_bounding_rect(self):
        """A square bounding box around the circle."""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
