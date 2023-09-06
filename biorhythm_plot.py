#!/usr/bin/env python3
""" A Python module for generating a biorhythm chart.
Plots a chart of physical, emotional, and intellectual cycles using Matplotlib
and NumPy to render an image.  The secondary cycles of spiritual, intuition,
awareness and aesthetic can be optionally displayed.
https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)
History:
01.00 2023-Aug-17 Scott S. Initial release.
01.01 2023-Aug-18 Scott S. Added the secondary cycles.

MIT License

Copyright (c) 2023 TigerPointe Software, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

FOR ENTERTAINMENT PURPOSES ONLY.

Create a custom get_bio.py file for your own birthday or favorite celebrity.

#!/usr/bin/env python3
# Penny Singleton was an American actress and labor
# leader.  During her 60-year career on stage, screen,
# radio and television, Singleton appeared as the
# comic-strip heroine Blondie Bumstead in a series of
# 28 motion pictures from 1938 until 1950 and the
# popular Blondie radio program from 1939 until 1950.
# Singleton also provided the voice of Jane Jetson in
# the animated series The Jetsons from 1962 to 1963.
# https://en.wikipedia.org/wiki/Penny_Singleton
import biorhythm_plot as bp
bp.main(year=1908, month=9, day=15)

Create a custom get_bio.py file to open multiple windows concurrently.

#!/usr/bin/env python3
import biorhythm_plot as bp
bp.main(year=1908, month=9, day=15, block=False)
bp.main(year=1908, month=9, day=15, block=False,
        physical=False, emotional=False, intellectual=False,
        spiritual=True, intuition=True, awareness=True, aesthetic=True)
input('Press ENTER to Continue: ')

If you enjoy this software, please do something kind for free.

Please consider giving to cancer research.
https://braintumor.org/
https://www.cancer.org/
"""

from datetime import datetime
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np


def get_bio(birthdate=np.datetime64('today'),
            plotdate=np.datetime64('today'),
            physical=False, emotional=False,
            intellectual=False, spiritual=False,
            intuition=False, awareness=False,
            aesthetic=False, days=29,
            block=True):
    """ Gets a biorhythm chart.
    PARAMETERS:
    birthdate    : the NumPy birth date of the person
    plotdate     : the NumPy plot date of the chart
    physical     : show the physical cycle
    emotional    : show the emotional cycle
    intellectual : show the intellectual cycle
    spiritual    : show the spiritual cycle
    intuition    : show the intuition cycle
    awareness    : show the awareness cycle
    aesthetic    : show the aesthetic cycle
    days         : the number of days to plot
    block        : block the process while the chart window is open
    """

    # Define the output date and number formats
    longdate = '%A, %B %d, %Y'  # Wednesday, January 31, 1900
    shortdate = '%a %b %d'      # Wed Jan 31
    number = '{:,}'             # 9,999

    # Define the primary wavelengths (days per cycle)
    # https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)
    pwave = 23  # physical
    ewave = 28  # emotional
    iwave = 33  # intellectual

    # Define the secondary wavelengths (days per cycle)
    sp2wave = 53  # spiritual
    in2wave = 38  # intuition
    aw2wave = 48  # awareness
    ae2wave = 43  # aesthetic

    # Sanity check (minimum days to plot)
    if (days < 3):
        days = 3

    # Calculate the midpoint of the chart
    middays = math.floor(days / 2)

    # Calculate the sets of date values and day counts since birth
    lowdate = plotdate - np.timedelta64(middays, 'D')
    dates = np.array([lowdate + np.timedelta64(x, 'D') for x in range(days)],
                     dtype=np.datetime64)
    counts = np.array(dates - birthdate, dtype=np.int64)

    # Calculate the primary sets of point values
    # https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)#Calculation
    # Sine oscillates between -1 and +1 as increasing radian values are
    # passed; the angle value is calculated using 2*PI, which is the
    # number of radians in a circle; the official calculation specifies to
    # then multiply by the number of days since birth and divide by the
    # wavelength; the resulting amplitude will be a decimal value which
    # occurs somewhere between -1 and +1
    cycles = 0
    pvalues = None
    if physical:
        pvalues = np.sin((counts * 2 * np.pi) / pwave, dtype=np.float64)
        cycles += 1
    evalues = None
    if emotional:
        evalues = np.sin((counts * 2 * np.pi) / ewave, dtype=np.float64)
        cycles += 1
    ivalues = None
    if intellectual:
        ivalues = np.sin((counts * 2 * np.pi) / iwave, dtype=np.float64)
        cycles += 1

    # Calculate the secondary sets of point values
    sp2values = None
    if spiritual:
        sp2values = np.sin((counts * 2 * np.pi) / sp2wave, dtype=np.float64)
        cycles += 1
    in2values = None
    if intuition:
        in2values = np.sin((counts * 2 * np.pi) / in2wave, dtype=np.float64)
        cycles += 1
    aw2values = None
    if awareness:
        aw2values = np.sin((counts * 2 * np.pi) / aw2wave, dtype=np.float64)
        cycles += 1
    ae2values = None
    if aesthetic:
        ae2values = np.sin((counts * 2 * np.pi) / ae2wave, dtype=np.float64)
        cycles += 1

    # Sanity check (cycles to plot)
    if (cycles < 1):
        raise ValueError('No cycles were specified for display.')

    # Create the data labels
    plot = plotdate.item().strftime(longdate)
    birth = birthdate.item().strftime(longdate)
    count = number.format(counts[middays])

    # Create a new figure measured in inches (100px per inch)
    plt.figure(figsize=(10, 4.5))
    plt.gcf().canvas.manager.set_window_title('biorhythm')

    # Set the title
    plt.title('Biorhythm for {plot}'.format(plot=plot), fontsize=16)

    # Include the birth date information
    info = 'Birth:  {birth} ({count} days)'.format(birth=birth, count=count)
    plt.gcf().text(0.1, 0.89, info, fontsize=8)

    # Set the x-axis labels
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(shortdate))
    plt.xlabel('Date', fontsize=10)
    plt.xticks(dates, rotation=90, fontsize=8)

    # Set the y-axis labels
    plt.gca().yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    plt.ylabel('Passive  Critical  Active', fontsize=10)

    # Enable the grid lines
    plt.grid(alpha=0.35)

    # Highlight the current day (y = yellow)
    plt.axvspan(dates[middays - 1], dates[middays + 1], color='y', alpha=0.15)

    # Plot the primary data values
    if pvalues is not None:
        plt.plot(dates, pvalues, label='Physical', linewidth=2, marker='_')
    if evalues is not None:
        plt.plot(dates, evalues, label='Emotional', linewidth=2, marker='_')
    if ivalues is not None:
        plt.plot(dates, ivalues, label='Intellectual', linewidth=2, marker='_')

    # Plot the secondary data values
    if sp2values is not None:
        plt.plot(dates, sp2values, label='Spiritual', linewidth=2, marker='_')
    if in2values is not None:
        plt.plot(dates, in2values, label='Intuition', linewidth=2, marker='_')
    if aw2values is not None:
        plt.plot(dates, aw2values, label='Awareness', linewidth=2, marker='_')
    if ae2values is not None:
        plt.plot(dates, ae2values, label='Aesthetic', linewidth=2, marker='_')

    # Show the legend
    plt.legend(bbox_to_anchor=(1.0, 1.0), loc='upper left', fontsize=10)

    # Optimize the padding and show the chart
    plt.tight_layout()
    plt.show(block=block)


def main(year=datetime.now().year,
         month=datetime.now().month,
         day=datetime.now().day,
         physical=True, emotional=True,
         intellectual=True, spiritual=False,
         intuition=False, awareness=False,
         aesthetic=False, block=True):
    """ Defines the main entry point of the program.
    PARAMETERS:
    year         : the birth year of the person (0001-9999)
    month        : the birth month of the person (1-12)
    day          : the birth day of the person (1-31)
    physical     : show the physical cycle
    emotional    : show the emotional cycle
    intellectual : show the intellectual cycle
    spiritual    : show the spiritual cycle
    intuition    : show the intuition cycle
    awareness    : show the awareness cycle
    aesthetic    : show the aesthetic cycle
    block        : block the process while the chart window is open
    """

    # Combine the integers into a NumPy compatible date
    y = str(year).zfill(4)[:4]
    m = str(month).zfill(2)[:2]
    d = str(day).zfill(2)[:2]
    birthdate = '{year}-{month}-{day}'.format(year=y, month=m, day=d)
    get_bio(birthdate=np.datetime64(birthdate),
            physical=physical, emotional=emotional,
            intellectual=intellectual, spiritual=spiritual,
            intuition=intuition, awareness=awareness,
            aesthetic=aesthetic, block=block)


# Start the program interactively
if __name__ == '__main__':
    try:
        print('Biorhythm:')
        year = int(input('  Enter your birth YEAR (0001-9999): '))
        month = int(input('  Enter your birth MONTH (1-12): '))
        day = int(input('  Enter your birth DAY (1-31): '))
        main(year=year, month=month, day=day)
    except Exception as e:
        print(str(e))
