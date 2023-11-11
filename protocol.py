from __future__ import annotations

from typing import Protocol
from pygame.event import Event
from pygame import Surface, Vector2
from pygame.key import ScancodeWrapper

class ConvexShapeProtocol(Protocol):
    def draw(self,screen: Surface):
        ...

    def _polygon(self):
        ...

    def collides(self,shape: ConvexShapeProtocol):
        other_poly = shape._polygon()
        poly = self._polygon()

        return polygons_collide(poly, other_poly)


class MovingShapeProtocol(Protocol):
    def update(self, dt: float):
        ...

    def get_collider(self) -> ConvexShapeProtocol:
        ...

def find_axes(polygon):
    axes = []
    for i in range(len(polygon)):
        # Get two neighboring points
        p1 = polygon[i]
        p2 = polygon[(i + 1) % len(polygon)]
        # Compute the edge vector
        edge = Vector2(p2) - Vector2(p1)
        # Get the perpendicular vector (normal)
        normal = Vector2(-edge.y, edge.x).normalize()
        axes.append(normal)
    return axes

def project_polygon(axis, polygon):
    min_proj = float('inf')
    max_proj = float('-inf')
    for point in polygon:
        proj = Vector2(point).dot(axis)
        min_proj = min(min_proj, proj)
        max_proj = max(max_proj, proj)
    return min_proj, max_proj

def is_overlapping(minA, maxA, minB, maxB):
    return maxA >= minB and maxB >= minA

def polygons_collide(poly1, poly2):
    for polygon in [poly1, poly2]:
        axes = find_axes(polygon)
        for axis in axes:
            minA, maxA = project_polygon(axis, poly1)
            minB, maxB = project_polygon(axis, poly2)
            if not is_overlapping(minA, maxA, minB, maxB):
                # Found a separating axis
                return False
    # No separating axis found, polygons must be intersecting
    return True
