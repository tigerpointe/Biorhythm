#!/usr/bin/env python3
""" A Python module for generating a detailed biorhythm chart.

MIT License

Copyright (c) 2025 TigerPointe Software, LLC

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

Please consider giving to cancer research.
https://braintumor.org/
https://www.cancer.org/
"""
from datetime import datetime, timedelta
from math import floor, pi, sin


def get_data(birth=datetime.now(), plot=datetime.now(), days=7):
    """ Gets the calculated physical, emotional, and intellectual data.
    PARAMETERS:
    birth : birth date of the person
    plot  : plot date of the chart
    days  : number of days to include before and after the plot date
    RETURNS:
    The physical, emotional, and intellectual data
    """
    data = []
    dates = (plot + timedelta(days=d) for d in range(-days, days + 1))
    for d in dates:
        n = (d - birth).days  # number of days since birth
        p = sin(2 * pi * n / 23)  # physical
        e = sin(2 * pi * n / 28)  # emotional
        i = sin(2 * pi * n / 33)  # intellectual
        data.append((d, n, p, e, i))  # extra parentheses, appends tuple
    return data


def plot_chart(birth=datetime.now(), plot=datetime.now(), width=25, days=7):
    """ Plots a chart of physical, emotional, and intellectual cycles.
    PARAMETERS:
    birth : birth date of the person
    plot  : plot date of the chart
    width : width of the chart in characters
    days  : number of days to show before and after the plot date
    REMARKS:
    The output is optimized for a traditional 80x24 console window.
    The chart width and days range can be changed to fit your system.
    """
    width = 15 if width < 15 else width
    midwidth = floor(width / 2)
    print('BIORHYTHM for Birth Date:', f'{birth:%A, %d %B %Y}')
    print('p=physical, e=emotional, i=intellectual for days since birth')
    print('Date', ' ' * 10, '-100%', '=' * (width - 12), '+100%',
          '   p   ', '   e   ', '   i   ', 'Day')
    data = get_data(birth=birth, plot=plot, days=days)
    for d, n, p, e, i in data:
        _p = midwidth + floor(p * (midwidth - 1))  # from middle zero, add
        _e = midwidth + floor(e * (midwidth - 1))  # -/+ percentages of width
        _i = midwidth + floor(i * (midwidth - 1))  # to reach -100% or +100%
        out = list(('-' if d.date() == plot.date() else ' ') * width)
        out[midwidth] = ':'
        out[_p] = '*' if _p in {_e, _i} else 'p'  # overlapping values
        out[_e] = '*' if _e in {_i, _p} else 'e'
        out[_i] = '*' if _i in {_p, _e} else 'i'
        print(f'{d:%a %d %b %Y}', ''.join(out),
              f'{f"{p:+.1%}":>7}',  # nested percentage and alignment formats
              f'{f"{e:+.1%}":>7}',
              f'{f"{i:+.1%}":>7}',
              f'{n:,}')


if __name__ == '__main__':
    year = int(input('Enter your birth YEAR (0001-9999): '))
    month = int(input('Enter your birth MONTH (1-12): '))
    day = int(input('Enter your birth DAY (1-31): '))
    width = int(input('Enter the chart WIDTH (default=25): ') or '25')
    days = int(input('Enter the before/after DAYS (default=7): ') or '7')
    plot_chart(birth=datetime(year, month, day), width=width, days=days)
    input('Press ENTER to Continue: ')
