#!/usr/bin/env python3
""" A super simple Python module for generating a biorhythm chart.

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
"""
from datetime import datetime, timedelta
from math import floor, pi, sin


def get_bio(birth=datetime.now(), plot=datetime.now(), width=45, days=14):
    """ Plots a chart of physical, emotional, and intellectual cycles.
    PARAMETERS:
    birth : birth date of the person
    plot  : plot date of the chart
    width : width of the chart in characters
    days  : number of days to show before and after the plot date
    """
    width = 15 if width < 15 else width
    midwidth = floor(width / 2)
    print('BIORHYTHM for Birth Date:', f'{birth:%A, %d %B %Y}')
    print('p=physical, e=emotional, i=intellectual for days since birth')
    print('Date', ' ' * 10, '-100%', '=' * (width - 12), '+100%', 'Day')
    dates = (plot + timedelta(days=d) for d in range(-days, days + 1))
    for d in dates:
        n = (d - birth).days
        p = midwidth + floor(sin(2 * pi * n / 23) * (midwidth - 1))
        e = midwidth + floor(sin(2 * pi * n / 28) * (midwidth - 1))
        i = midwidth + floor(sin(2 * pi * n / 33) * (midwidth - 1))
        out = list(('-' if d.date() == plot.date() else ' ') * width)
        out[midwidth] = ':'
        out[p] = '*' if p in {e, i} else 'p'
        out[e] = '*' if e in {i, p} else 'e'
        out[i] = '*' if i in {p, e} else 'i'
        print(f'{d:%a %d %b %Y}', ''.join(out), f'{n:,}')


if __name__ == '__main__':
    year = int(input('Enter your birth YEAR (0001-9999): '))
    month = int(input('Enter your birth MONTH (1-12): '))
    day = int(input('Enter your birth DAY (1-31): '))
    get_bio(birth=datetime(year, month, day))
    input('Press ENTER to Continue: ')
