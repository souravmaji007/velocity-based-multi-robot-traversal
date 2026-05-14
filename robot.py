import random
import math

from config import *


class Robot:

    def __init__(self, x, y, name):

        self.x = x
        self.y = y

        self.name = name

        self.speed = random.uniform(1, 3)

        self.target_x = random.randint(
            0,
            COLS - 1
        ) * GRID_SIZE

        self.target_y = random.randint(
            0,
            ROWS - 1
        ) * GRID_SIZE

        self.completed = False

        self.distance_travelled = 0


        # CURRENT VELOCITY

        self.vx = 0
        self.vy = 0


        # STUCK DETECTION

        self.last_x = x
        self.last_y = y

        self.stuck_counter = 0


    # =====================================
    # MAIN MOVEMENT FUNCTION
    # =====================================

    def move(
        self,
        robots,
        safe_distance,
        moving_obstacles
    ):

        if self.completed:
            return


        # =====================================
        # STUCK DETECTION
        # =====================================

        movement_check = math.hypot(
            self.x - self.last_x,
            self.y - self.last_y
        )

        if movement_check < 1:

            self.stuck_counter += 1

        else:

            self.stuck_counter = 0


        self.last_x = self.x
        self.last_y = self.y


        # =====================================
        # TARGET DIRECTION
        # =====================================

        dx = self.target_x - self.x
        dy = self.target_y - self.y

        dist = math.hypot(dx, dy)


        # TARGET REACHED

        if dist <= self.speed:

            self.x = self.target_x
            self.y = self.target_y

            self.completed = True

            return


        # =====================================
        # BASE VELOCITY
        # =====================================

        move_x = (dx / dist) * self.speed
        move_y = (dy / dist) * self.speed


        # =====================================
        # STUCK RECOVERY MODE
        # =====================================

        if self.stuck_counter > 20:

            move_x = random.choice(
                [-1, 1]
            ) * self.speed * 2

            move_y = random.choice(
                [-1, 1]
            ) * self.speed * 2

            self.stuck_counter = 0


        # =====================================
        # FUTURE POSITION PREDICTION
        # =====================================

        future_x = self.x + move_x * 5
        future_y = self.y + move_y * 5


        # =====================================
        # ROBOT COLLISION PREDICTION
        # =====================================

        for robot in robots:

            if robot == self:
                continue


            future_robot_x = robot.x + robot.vx * 5
            future_robot_y = robot.y + robot.vy * 5


            future_dist = math.hypot(
                future_x - future_robot_x,
                future_y - future_robot_y
            )


            # VELOCITY OBSTACLE AVOIDANCE

            if future_dist < safe_distance:


                angle = random.uniform(
                    -math.pi / 4,
                    math.pi / 4
                )

                cos_a = math.cos(angle)
                sin_a = math.sin(angle)


                rotated_x = (
                    move_x * cos_a -
                    move_y * sin_a
                )

                rotated_y = (
                    move_x * sin_a +
                    move_y * cos_a
                )


                move_x = rotated_x
                move_y = rotated_y


        # =====================================
        # MOVING OBSTACLE AVOIDANCE
        # =====================================

        for obs in moving_obstacles:


            future_obs_x = obs.x + obs.dx * 5
            future_obs_y = obs.y + obs.dy * 5


            obs_dist = math.hypot(
                future_x - future_obs_x,
                future_y - future_obs_y
            )


            if obs_dist < safe_distance * 2:


                move_x += random.choice(
                    [-1, 1]
                ) * self.speed

                move_y += random.choice(
                    [-1, 1]
                ) * self.speed


                move_x *= 0.7
                move_y *= 0.7


        # =====================================
        # STATIC SHELF AVOIDANCE
        # =====================================

        next_x = self.x + move_x
        next_y = self.y + move_y


        for obs in OBSTACLES:

            ox, oy, ow, oh = obs


            if (
                ox <= next_x <= ox + ow and
                oy <= next_y <= oy + oh
            ):


                # SLIDE AROUND OBSTACLE

                if abs(dx) > abs(dy):

                    move_y += random.choice(
                        [-1, 1]
                    ) * self.speed

                else:

                    move_x += random.choice(
                        [-1, 1]
                    ) * self.speed


                # SMALL VELOCITY REDUCTION

                move_x *= 0.8
                move_y *= 0.8


        # =====================================
        # UPDATE VELOCITY
        # =====================================

        self.vx = move_x
        self.vy = move_y


        # =====================================
        # UPDATE POSITION
        # =====================================

        self.x += move_x
        self.y += move_y


        # =====================================
        # WAREHOUSE BOUNDARY CHECK
        # =====================================

        self.x = max(
            0,
            min(self.x, WIDTH)
        )

        self.y = max(
            0,
            min(self.y, HEIGHT)
        )


        # =====================================
        # DISTANCE TRACKING
        # =====================================

        self.distance_travelled += math.hypot(
            move_x,
            move_y
        )