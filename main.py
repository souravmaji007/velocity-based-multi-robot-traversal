import matplotlib.pyplot as plt
import matplotlib.animation as animation

from robot import Robot
from metrics import Metrics
from config import *
from obstacle import MovingObstacle

import time
import random
import math
import os


# ==========================================
# CREATE OUTPUT FOLDER
# ==========================================

if not os.path.exists("outputs"):
    os.makedirs("outputs")


# ==========================================
# USER INPUT PARAMETERS
# ==========================================

def get_user_params():

    try:

        num_robots = int(
            input("Enter number of robots (default 5): ") or 5
        )

        max_speed_mpm = float(
            input(
                f"Enter max speed (meters/min) default {MAX_SPEED}: "
            ) or MAX_SPEED
        )

        safe_distance_m = float(
            input("Enter safe distance (meters): ") or 3
        )

        time_step_min = float(
            input("Enter timestep (minutes): ") or 0.001
        )

    except:

        print("Invalid input. Using defaults.")

        num_robots = 5
        max_speed_mpm = MAX_SPEED
        safe_distance_m = 3
        time_step_min = 0.001


    # SPEED CONVERSION

    max_speed = max_speed_mpm / 2

    safe_distance = safe_distance_m * GRID_SIZE

    time_step = time_step_min * 60


    return (
        num_robots,
        max_speed,
        safe_distance,
        time_step
    )


(
    num_robots,
    max_speed,
    safe_distance,
    time_step
) = get_user_params()


# ==========================================
# ROBOT INITIALIZATION
# ==========================================

robots = []

for i in range(num_robots):

    while True:

        x = random.randint(
            0,
            COLS - 1
        ) * GRID_SIZE

        y = random.randint(
            0,
            ROWS - 1
        ) * GRID_SIZE

        inside_obstacle = False

        for obs in OBSTACLES:

            ox, oy, ow, oh = obs

            if (
                ox <= x <= ox + ow and
                oy <= y <= oy + oh
            ):

                inside_obstacle = True


        if not inside_obstacle:
            break


    robot = Robot(
        x,
        y,
        f"R{i+1}"
    )

    robot.speed = max_speed

    robots.append(robot)


# ==========================================
# MOVING OBSTACLES
# ==========================================

moving_obstacles = []

for obs in MOVING_OBSTACLES:

    moving_obstacles.append(

        MovingObstacle(
            obs["x"],
            obs["y"],
            obs["dx"],
            obs["dy"],
            obs["size"]
        )
    )


# ==========================================
# TRACKING
# ==========================================

metrics = Metrics()

robot_positions = {
    r.name: [(r.x, r.y)]
    for r in robots
}

obstacle_positions = []

start_time = time.time()


# ==========================================
# SIMULATION LOOP
# ==========================================

max_steps = 5000

for step in range(max_steps):


    # MOVE DYNAMIC OBSTACLES

    current_obs_positions = []

    for obs in moving_obstacles:

        obs.move()

        current_obs_positions.append(
            (obs.x, obs.y)
        )

    obstacle_positions.append(
        current_obs_positions
    )


    # MOVE ROBOTS

    for robot in robots:

        robot.move(
            robots,
            safe_distance,
            moving_obstacles
        )

        robot_positions[robot.name].append(
            (robot.x, robot.y)
        )


    # CHECK COMPLETION

    if all(r.completed for r in robots):

        print(
            f"\nAll robots completed in {step+1} steps."
        )

        break


    time.sleep(0.001)


end_time = time.time()


# ==========================================
# METRICS
# ==========================================

data = metrics.calculate(robots)

data["Simulation Time"] = round(
    end_time - start_time,
    2
)

print("\n===== SIMULATION METRICS =====")

for key, value in data.items():

    print(f"{key}: {value}")

print("================================")


# ==========================================
# PATH VERIFICATION
# ==========================================

def verify_paths(robots, robot_positions):

    print("\n===== PATH VERIFICATION =====")

    success_count = 0

    for r in robots:

        final_pos = robot_positions[r.name][-1]

        target = (
            r.target_x,
            r.target_y
        )

        dist = math.hypot(
            final_pos[0] - target[0],
            final_pos[1] - target[1]
        )

        if dist > 25:

            print(
                f"[ERROR] {r.name} failed."
            )

        else:

            print(
                f"[OK] {r.name} reached target."
            )

            success_count += 1


    success_rate = (
        success_count / len(robots)
    ) * 100

    print(
        f"\nSUCCESS RATE: {success_rate:.2f}%"
    )


verify_paths(
    robots,
    robot_positions
)


# ==========================================
# STATIC VISUALIZATION
# ==========================================

plt.figure(figsize=(12, 8))

colors = [
    'blue',
    'red',
    'magenta',
    'cyan',
    'green',
    'orange',
    'purple'
]


# ROBOT PATHS

for i, r in enumerate(robots):

    positions = robot_positions[r.name]

    xs, ys = zip(*positions)

    plt.plot(
        xs,
        ys,
        linewidth=4,
        color=colors[i % len(colors)],
        alpha=0.8,
        label=f"{r.name} Path"
    )

    plt.plot(
        positions[0][0],
        positions[0][1],
        marker='s',
        markersize=10,
        color=colors[i % len(colors)]
    )

    plt.plot(
        r.target_x,
        r.target_y,
        marker='*',
        markersize=15,
        color=colors[i % len(colors)],
        label=f"{r.name} Target"
    )


# GRID

for x in range(0, WIDTH + 1, GRID_SIZE):

    plt.axvline(
        x,
        color='gray',
        linewidth=0.5
    )

for y in range(0, HEIGHT + 1, GRID_SIZE):

    plt.axhline(
        y,
        color='gray',
        linewidth=0.5
    )


# STATIC OBSTACLES

for obs in OBSTACLES:

    ox, oy, ow, oh = obs

    rect = plt.Rectangle(
        (ox, oy),
        ow,
        oh,
        color='black',
        alpha=0.7
    )

    plt.gca().add_patch(rect)


# MOVING OBSTACLES

for obs in moving_obstacles:

    circle = plt.Circle(
        (obs.x, obs.y),
        obs.size,
        color='red'
    )

    plt.gca().add_patch(circle)


plt.title(
    "Velocity Obstacle Based Multi-Robot Traversal"
)

plt.xlabel("X Position")
plt.ylabel("Y Position")

plt.legend()
plt.grid(True)


# SAVE PNG

png_filename = (
    f"outputs/robot_output_{int(time.time())}.png"
)

plt.savefig(
    png_filename,
    bbox_inches='tight'
)

print(f"\nPNG saved: {png_filename}")


# ==========================================
# GIF ANIMATION
# ==========================================

fig, ax = plt.subplots(figsize=(12, 8))

ax.set_xlim(0, WIDTH)
ax.set_ylim(0, HEIGHT)

ax.set_title(
    "Robot Traversal Animation"
)

ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")


# GRID

for x in range(0, WIDTH + 1, GRID_SIZE):

    ax.axvline(
        x,
        color='gray',
        linewidth=0.5
    )

for y in range(0, HEIGHT + 1, GRID_SIZE):

    ax.axhline(
        y,
        color='gray',
        linewidth=0.5
    )


# STATIC OBSTACLES

for obs in OBSTACLES:

    ox, oy, ow, oh = obs

    rect = plt.Rectangle(
        (ox, oy),
        ow,
        oh,
        color='black',
        alpha=0.7
    )

    ax.add_patch(rect)


# MOVING OBSTACLES

moving_obs_draw = []

for obs in moving_obstacles:

    circle = plt.Circle(
        (obs.x, obs.y),
        obs.size,
        color='red'
    )

    ax.add_patch(circle)

    moving_obs_draw.append(circle)


# ROBOT OBJECTS

robot_dots = []
path_lines = []


for i, r in enumerate(robots):

    dot, = ax.plot(
        [],
        [],
        'o',
        markersize=8,
        color=colors[i % len(colors)],
        label=r.name
    )

    line, = ax.plot(
        [],
        [],
        linewidth=4,
        color=colors[i % len(colors)]
    )

    robot_dots.append(dot)
    path_lines.append(line)

    ax.plot(
        r.target_x,
        r.target_y,
        '*',
        markersize=15,
        color=colors[i % len(colors)]
    )


ax.legend()


# ==========================================
# ANIMATION UPDATE
# ==========================================

def update(frame):


    # UPDATE MOVING OBSTACLES

    if frame < len(obstacle_positions):

        for i, pos in enumerate(
            obstacle_positions[frame]
        ):

            moving_obs_draw[i].center = pos


    # UPDATE ROBOTS

    for i, r in enumerate(robots):

        positions = robot_positions[r.name]

        if frame < len(positions):

            xs = [
                p[0]
                for p in positions[:frame+1]
            ]

            ys = [
                p[1]
                for p in positions[:frame+1]
            ]

            path_lines[i].set_data(
                xs,
                ys
            )

            robot_dots[i].set_data(
                [positions[frame][0]],
                [positions[frame][1]]
            )


    return (
        robot_dots +
        path_lines +
        moving_obs_draw
    )


# TOTAL FRAMES

frames = max(
    len(robot_positions[r.name])
    for r in robots
)


# CREATE GIF

ani = animation.FuncAnimation(
    fig,
    update,
    frames=frames,
    interval=40,
    blit=True
)


# SAVE GIF

gif_filename = (
    f"outputs/robot_animation_{int(time.time())}.gif"
)

ani.save(
    gif_filename,
    writer='pillow'
)

print(f"\nGIF saved: {gif_filename}")


plt.show()