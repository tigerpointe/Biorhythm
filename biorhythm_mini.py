#!/usr/bin/env python3
""" A minimalist Python module for generating a biorhythm chart.
https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)
History:
01.00 2025-Jan-01 Scott S. Initial release.
01.01 2025-Jan-20 Scott S. Added verbose mode.

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


def get_bio(birth=dt.now(), plot=dt.now(), width=45, days=7, verbose=True):
    pwave, ewave, iwave = 23, 28, 33  # physical, emotional, intellectual
    width = 15 if width < 15 else width  # minimum chart width enforced
    midwidth = floor(width / 2)  # middle point of chart, distance to edge
    print('BIORHYTHM for Birth Date:', birth.strftime('%A, %d %B %Y'))
    print('p=physical, e=emotional, i=intellectual for days since birth')
    print('-100%', '=' * (width - 12), '+100%')  # literal lengths subtracted
    dates = (plot + td(days=d) for d in range(-days, days + 1))
    for d in dates:
        n = (d - birth).days  # number of days since birth
        # sine models -/+ percentages of distance from middle point of chart
        _p = sin(2 * pi * n / pwave)
        _e = sin(2 * pi * n / ewave)
        _i = sin(2 * pi * n / iwave)
        p = midwidth + floor(_p * (midwidth - 1))
        e = midwidth + floor(_e * (midwidth - 1))
        i = midwidth + floor(_i * (midwidth - 1))
        out = list(('-' if d.date() == plot.date() else ' ') * width)
        out[midwidth] = ':'
        out[p] = '*' if p in {e, i} else 'p'
        out[e] = '*' if e in {i, p} else 'e'
        out[i] = '*' if i in {p, e} else 'i'
        print(''.join(out), d.strftime('%a %d %b %Y,'), 'Day={:,}'.format(n))
        if verbose:
            print(' ' * width,
                  f'p:{_p*100:+.1f}%  e:{_e*100:+.1f}%  i:{_i*100:+.1f}%')


if __name__ == '__main__':
    year = int(input('Enter your birth YEAR (0001-9999): '))
    month = int(input('Enter your birth MONTH (1-12): '))
    day = int(input('Enter your birth DAY (1-31): '))
    get_bio(birth=dt(year, month, day))
    input('\nPress ENTER to Continue: ')
