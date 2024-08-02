from typing import List, Tuple, Union, TypedDict
import random
import math


"""
At some point, upgrade this algorithm to generate more human-like motions.
"""


class LocationData(TypedDict):
    """Location data related to game type 4 components.

    Attributes:
        left_arrow (Tuple[int, int]): The x and y coordinates of the left arrow.
        right_arrow (Tuple[int, int]): The x and y coordinates of the right arrow.
        submit_button (Tuple[int, int]): The x and y coordinates of the submit button.
    """

    left_arrow: Tuple[int, int]
    right_arrow: Tuple[int, int]
    submit_button: Tuple[int, int]


class Points(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @staticmethod
    def make_bezier(control_points: List[Tuple[float, float]]) -> callable:
        """
        Creates a Bezier curve function based on the given control points.
        """

        def pascal_row(n: int) -> List[float]:
            """
            Generates the nth row of Pascal's triangle.
            """

            row = [1]
            for k in range(1, n + 1):
                row.append(row[-1] * (n - k + 1) // k)

            return row

        n = len(control_points) - 1
        coefficients = pascal_row(n)

        def bezier(t_values: List[float]) -> List[Tuple[int, int]]:
            """
            Generates points on the Bezier curve for the given parameter values.
            """
            points = []
            for t in t_values:
                tpowers = [t**i for i in range(n + 1)]
                upowers = [(1 - t) ** (n - i) for i in range(n + 1)]
                coefs = [
                    c * tp * up for c, tp, up in zip(coefficients, tpowers, upowers)
                ]
                points.append(
                    tuple(
                        round(sum(coef * p for coef, p in zip(coefs, ps)))
                        for ps in zip(*control_points)
                    )
                )

            return points

        return bezier

    @staticmethod
    def extract_significant_points(
        points: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """
        An algorithm Arkose Labs uses to extract significant points from all collected mouse movements.
        """
        if not points:
            return []

        significant_points = [points[0]]  # First point is automatically added
        for point in points[1:]:
            current_x, current_y = point
            last_x, last_y = significant_points[-1]

            if math.sqrt((current_x - last_x) ** 2 + (current_y - last_y) ** 2) > 5:
                significant_points.append(point)

        return significant_points

    @staticmethod
    def generate_bezier_path(
        coord_list: List[Tuple[int, int]], deviation: int, speed: Union[float, int]
    ) -> List[Tuple[int, int]]:
        """
        Generates a path composed of connected Bezier curves between given coordinates.

        Args:
            coord_list (List[Tuple[int, int]]): A list of coordinates to generate the path from
            deviation (int): The maximum deviation from the given coordinates
            speed (Union[float, int]): The speed at which the points are generated

        Returns:
            List[Tuple[int, int]]: A list of points representing the generated path.
        """

        path = []
        for start, end in zip(coord_list, coord_list[1:]):
            t_values = [t / (round(speed * 100.0)) for t in range(round(speed * 101))]

            def random_control_point(p1, p2):
                return (
                    p1[0]
                    + random.choice((-1, 1))
                    * abs(p2[0] - p1[0])
                    * 0.01
                    * random.randint(deviation // 2, deviation),
                    p1[1]
                    + random.choice((-1, 1))
                    * abs(p2[1] - p1[1])
                    * 0.01
                    * random.randint(deviation // 2, deviation),
                )

            control_1 = random_control_point(start, end)
            control_2 = random_control_point(start, end)
            bezier = Points.make_bezier([start, control_1, control_2, end])
            path.extend(bezier(t_values))

        return Points.extract_significant_points(path)

    def generate_point_around(self, threshold: int) -> Tuple[int, int]:
        """Generates a random point *around* the current point within a specified threshold distance, in pixels.

        Args:
            threshold (int): maximum distance from the current point

        Returns:
            Tuple[int, int]: A tuple containing the x and y coordinates of the generated point
        """

        angle, radius = random.uniform(0, 2 * math.pi), random.uniform(0, threshold)

        return (
            round(self.x + radius * math.cos(angle)),
            round(self.y + radius * math.sin(angle)),
        )


def tile_to_location(
    tile: int, padding: int = 15, offset: Union[Tuple[int, int], None] = None
) -> Tuple[int, int]:
    """Calculates the pixel location for a given game type 4 tile index.

    Args:
        tile (int): The tile number on a 2x3 grid, indices start at 0.
        padding (int, optional): Additional padding (in pixels) to be added to the calculated position.
        offset (Union[Tuple[int, int], None], optional): A tuple of x and y offsets to be added to the calculated position.
                                                         If None, random offsets between
                                                         0 and 70 will be used. Defaults to None.

    Raises:
        ValueError: If `offset` is provided but does not contain exactly two elements (x, y).

    Returns:
        Tuple[int, int]: A list containing the x and y pixel positions for the tile.
    """

    axes = [tile % 3, math.floor(tile / 3)]
    default_axes_offsets = [random.randint(0, 70) for _ in range(len(axes))]

    if offset is not None and len(offset) != len(axes):
        raise ValueError("Coordinate offset should be array [x, y]")

    return tuple(
        (
            axis * 100  # Each answer in the tile image is 100 x 100 pixels
            + axis * 3
            + padding
            + axis_offset
        )
        for axis, axis_offset in zip(axes, offset or default_axes_offsets)
    )
