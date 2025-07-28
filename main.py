from skyfield.api import load
import matplotlib.pyplot as plt
import numpy
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use('MacOSX') # Replace with 'TkAgg' or 'Qt5Agg' if windows/linux

def main():
    eph = load('de421.bsp')

    sun = eph['sun']
    mercury = eph['mercury']
    venus = eph['venus']
    earth = eph['earth']


    ts = load.timescale()
    days = numpy.arange(1, 364, 0.5)
    t = ts.utc(2025, 1, days)

    earth_pos = sun.at(t).observe(earth).position.km
    venus_pos = sun.at(t).observe(venus).position.km
    mercury_pos = sun.at(t).observe(mercury).position.km

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title("Inner solar system (Animated)")
    ax.set_xlabel('x (km)')
    ax.set_ylabel('y (km)')
    ax.set_aspect('equal')
    ax.grid(True)


    lim = 155_000_000
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)

    # Define planet info: name, color, position array
    planets = [
        {"name": "Earth",   "color": "b", "pos": earth_pos},
        {"name": "Venus",   "color": "y", "pos": venus_pos},
        {"name": "Mercury", "color": "g", "pos": mercury_pos},
    ]

    # Store plot elements for each planet
    planet_dots = {}
    planet_trails = {}
    planet_labels = {}

    for planet in planets:
        dot, = ax.plot([], [], f'{planet["color"]}o', label=planet["name"])
        trail, = ax.plot([], [], f'{planet["color"]}-', alpha=0.5)
        label = ax.text(0, 0, planet["name"], color=planet["color"], fontsize=10, ha='left', va='bottom')
        planet_dots[planet["name"]] = dot
        planet_trails[planet["name"]] = trail
        planet_labels[planet["name"]] = label

    sun_dot, = ax.plot(0, 0, 'ro', label='Sun')
    date_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, verticalalignment='top')

    def update(frame):
        for planet in planets:
            name = planet["name"]
            pos = planet["pos"]
            planet_dots[name].set_data([pos[0][frame]], [pos[1][frame]])
            planet_trails[name].set_data(pos[0][:frame+1], pos[1][:frame+1])
            planet_labels[name].set_position((pos[0][frame], pos[1][frame]))
        current_time = t[frame].utc_strftime('%Y-%m-%d')
        date_text.set_text(f"Date: {current_time}")
        return (
            list(planet_dots.values())
            + list(planet_trails.values())
            + list(planet_labels.values())
            + [date_text]
        )

    ani = FuncAnimation(fig, update, frames=len(earth_pos[0]), interval=50, blit=False)

    plt.legend()
    plt.show()


    
if __name__ == "__main__":
    main()