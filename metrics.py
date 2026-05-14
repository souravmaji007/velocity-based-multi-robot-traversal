class Metrics:

    def calculate(self, robots):

        completed = sum(1 for r in robots if r.completed)

        success_ratio = completed / len(robots)

        avg_velocity = sum(r.speed for r in robots) / len(robots)

        total_distance = sum(
            r.distance_travelled for r in robots
        )

        return {

            "Success Ratio": round(success_ratio, 2),

            "Average Velocity": round(avg_velocity, 2),

            "Total Distance": round(total_distance, 2)
        }