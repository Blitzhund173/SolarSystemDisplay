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
    ax.set_title("Earth Orbit Around Sun (Animated)")
    ax.set_xlabel('x (km)')
    ax.set_ylabel('y (km)')
    ax.set_aspect('equal')
    ax.grid(True)


    lim = 155_000_000
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)


    sun_dot, = ax.plot(0, 0, 'ro', label='Sun')
    earth_dot, = ax.plot([], [], 'bo', label='Earth')
    earthTrail, = ax.plot([], [], 'b-', alpha=0.5)

    venus_dot, = ax.plot([], [], 'yo', label='Venus')
    venusTrail, = ax.plot([], [], 'y-', alpha=0.5)

    mercury_dot, = ax.plot([], [], 'go', label='Mercury')
    mercuryTrail, = ax.plot([], [], 'g-', alpha=0.5)

    date_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, verticalalignment='top')

    def update(frame):
        earth_dot.set_data([earth_pos[0][frame]], [earth_pos[1][frame]])
        earthTrail.set_data(earth_pos[0][:frame+1], earth_pos[1][:frame+1])

        venus_dot.set_data([venus_pos[0][frame]], [venus_pos[1][frame]])
        venusTrail.set_data(venus_pos[0][:frame+1], venus_pos[1][:frame+1])

        mercury_dot.set_data([mercury_pos[0][frame]], [mercury_pos[1][frame]])
        mercuryTrail.set_data(mercury_pos[0][:frame+1], mercury_pos[1][:frame+1])

        current_time = t[frame].utc_strftime('%Y-%m-%d')
        date_text.set_text(f"Date: {current_time}")
        return earth_dot, earthTrail, date_text



    ani = FuncAnimation(fig, update, frames=len(earth_pos[0]), interval=50, blit=False)

    plt.legend()
    plt.show()


    
if __name__ == "__main__":
    main()