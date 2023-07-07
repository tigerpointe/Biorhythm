#!/usr/bin/env python3
""" A Python module for generating a biorhythm chart.
Plots a chart of physical, emotional, and intellectual cycles.
https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)
History:
01.00 2023-Jun-21 Scott S. Initial release.

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
import biorhythm
biorhythm.main(year=1908, month=9, day=15)
print()
input('Press ENTER to Continue: ')

If you enjoy this software, please do something kind for free.

Please consider giving to cancer research.
https://braintumor.org/
https://www.cancer.org/
"""

from datetime import datetime, timedelta
import math


def get_bio(birthdate=datetime.now(),
            plotdate=datetime.now(),
            width=50, days=29):
    """ Gets a biorhythm chart.
    PARAMETERS:
    birthdate : the birth date of the person
    plotdate  : the plot date of the chart
    width     : the width of the chart
    days      : the number of days to plot
    """

    # Define the output date and number formats
    longdate = '%a %b %d %Y'  # Wed Jan 31 1900
    shortdate = '%a %b %d'    # Wed Jan 31
    number = '{:,}'           # 9,999

    # Define the wavelengths (days per cycle)
    # https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)
    pwave = 23  # physical
    ewave = 28  # emotional
    iwave = 33  # intellectual

    # Sanity check (minimum width of the chart title)
    if (width < 12):
        width = 12

    # Calculate the midpoints of the chart
    midwidth = math.floor(width / 2)
    middays = math.floor(days / 2)

    # Count the number of days since birth
    count = (plotdate - birthdate).days

    # Write the chart header and label keys
    print('Birth:  ', birthdate.strftime(longdate), sep='')
    print('Plot:   ', plotdate.strftime(longdate), sep='')
    print('Alive:  ', number.format(count), ' days', sep='')
    print('p:      Physical')
    print('e:      Emotional')
    print('i:      Intellectual')

    # Write the chart title
    # The length of '-100% ' and ' +100%' equals 12 characters total
    title = 'PASSIVE  CRITICAL  ACTIVE'
    datepad = len(plotdate.strftime(shortdate)) + 1
    pad = datepad + midwidth                # chart center
    pad = pad - math.floor(len(title) / 2)  # title center
    print(' ' * pad, title, sep='')
    print(' ' * datepad, '-100% ', '=' * (width - 12), ' +100%', sep='')

    # Calculate the lowest date of the chart
    lowdate = plotdate - timedelta(middays)

    # Loop through each of the days
    for n in range(days):

        # Calculate the next day to plot
        nextdate = lowdate + timedelta(days=n)

        # Count the number of days since birth
        count = (nextdate - birthdate).days

        # Calculate the point values
        # https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)#Calculation
        # Sine oscillates between -1 and +1 as increasing radian values are
        # passed; the angle value is calculated using 2*PI, which is the
        # number of radians in a circle; the official calculation specifies to
        # then multiply by the number of days since birth and divide by the
        # wavelength; the resulting amplitude will be a decimal value which
        # occurs somewhere between -1 and +1
        pvalue = math.sin((2 * math.pi * count) / pwave)
        evalue = math.sin((2 * math.pi * count) / ewave)
        ivalue = math.sin((2 * math.pi * count) / iwave)

        # Calculate the point locations
        # The point values must be multiplied by half of the chart width to
        # calculate the final -/+ distance from the center line
        pindex = math.floor(pvalue * (midwidth - 1)) + midwidth
        eindex = math.floor(evalue * (midwidth - 1)) + midwidth
        iindex = math.floor(ivalue * (midwidth - 1)) + midwidth

        # Write the plot line, use an array of spaces equal to the chart width
        space = ' '
        if nextdate == plotdate:
            space = '-'
        out = list(space * width)
        out[midwidth] = ':'
        out[pindex] = 'p'
        out[eindex] = 'e'
        out[iindex] = 'i'
        if pindex == eindex:
            out[pindex] = '*'
        if eindex == iindex:
            out[eindex] = '*'
        if iindex == pindex:
            out[iindex] = '*'
        print(nextdate.strftime(shortdate), ''.join(out), sep=' ')


def main(year=datetime.now().year,
         month=datetime.now().month,
         day=datetime.now().day):
    """ Defines the main entry point of the program.
    PARAMETERS:
    year  : the birth year of the person (0001-9999)
    month : the birth month of the person (1-12)
    day   : the birth day of the person (0-31)
    """

    birthdate = datetime(year, month, day)
    get_bio(birthdate=birthdate)


# Start the program interactively
if __name__ == '__main__':
    try:
        print('Biorhythm:')
        year = int(input('  Enter your birth YEAR (0001-9999): '))
        month = int(input('  Enter your birth MONTH (1-12): '))
        day = int(input('  Enter your birth DAY (0-31): '))
        print()
        main(year=year, month=month, day=day)
    except Exception as e:
        print(str(e))
    print()
    input('Press ENTER to Continue: ')
