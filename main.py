from skyfield.api import load
import matplotlib.pyplot as plt
import numpy
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use('MacOSX') # Replace with 'TkAgg' or 'Qt5Agg' if windows/linux

def main():
    eph = load('de421.bsp')

    earth = eph['earth']
    moon = eph['moon']


    ts = load.timescale()
    days = numpy.arange(1, 364, 0.5)
    t = ts.utc(2025, 1, days)

    moon_pos = earth.at(t).observe(moon).position.km
    x,y,z = moon_pos


    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title("Moon Orbit Around Earth (Animated)")
    ax.set_xlabel("x (km)")
    ax.set_ylabel("y (km)")
    ax.set_aspect('equal')
    ax.grid(True)


    lim = 450_000
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)


    earth_dot, = ax.plot(0, 0, 'ro', label='Earth')
    trail, = ax.plot([], [], 'b-', alpha=0.5)
    moon_dot, = ax.plot([], [], 'bo', label='Moon')
    date_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12, verticalalignment='top')

    def update(frame):
        moon_dot.set_data([x[frame]], [y[frame]])
        trail.set_data(x[:frame+1], y[:frame+1])
        current_time = t[frame].utc_strftime('%Y-%m-%d')
        date_text.set_text(f"Date: {current_time}")
        return moon_dot, trail, date_text



    ani = FuncAnimation(fig, update, frames=len(x), interval=50, blit=False)

    plt.legend()
    plt.show()


    
if __name__ == "__main__":
    main()