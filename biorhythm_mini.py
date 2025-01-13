#!/usr/bin/env python3
""" A minimalist Python module for generating a biorhythm chart.
https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)
History:
01.00 2025-Jan-01 Scott S. Initial release.

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

FOR ENTERTAINMENT PURPOSES ONLY.

If you enjoy this software, please do something kind for free.

Please consider giving to cancer research.
https://braintumor.org/
https://www.cancer.org/
"""

from datetime import datetime as dt, timedelta as td
from math import floor, pi, sin


def get_bio(birth=dt.now(), plot=dt.now(), width=55, days=14):
    print('\nBIORHYTHM for Birth Date:', birth.strftime('%A, %d %B %Y'))
    pwave, ewave, iwave = 23, 28, 33  # physical, emotional, intellectual
    midx = floor(width / 2)  # middle of chart
    dates = (plot + td(days=d) for d in range(-days, days + 1))
    for d in dates:
        n = (d - birth).days  # number of days since birth
        # sine models -/+ percentages of distance from middle of chart
        p = midx + floor(sin(2 * pi * n / pwave) * (midx - 1))
        e = midx + floor(sin(2 * pi * n / ewave) * (midx - 1))
        i = midx + floor(sin(2 * pi * n / iwave) * (midx - 1))
        out = list(('-' if d.date() == plot.date() else ' ') * width)
        out[midx] = ':'
        out[p] = '*' if p in {e, i} else 'p'
        out[e] = '*' if e in {i, p} else 'e'
        out[i] = '*' if i in {p, e} else 'i'
        print(d.strftime('%a %d %b'), ''.join(out), '{:,}'.format(n))


if __name__ == '__main__':
    year = int(input('Enter your birth YEAR (0001-9999): '))
    month = int(input('Enter your birth MONTH (1-12): '))
    day = int(input('Enter your birth DAY (1-31): '))
    get_bio(birth=dt(year, month, day))
    input('\nPress ENTER to Continue: ')
