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

from datetime import datetime, timedelta
import math


def get_bio(birth=datetime.now(), plot=datetime.now(),  width=55, days=14):
    print('\nBIORHYTHM for Birth Date:', birth.strftime('%A, %d %B %Y'))
    pwave = 23  # physical
    ewave = 28  # emotional
    iwave = 33  # intellectual
    mid = math.floor(width / 2)  # middle line
    dates = [plot + timedelta(days=d) for d in range(-days, days + 1)]
    for d in dates:
        n = (d - birth).days  # number of days since birth
        p = math.floor(math.sin(2 * math.pi * n / pwave) * (mid - 1)) + mid
        e = math.floor(math.sin(2 * math.pi * n / ewave) * (mid - 1)) + mid
        i = math.floor(math.sin(2 * math.pi * n / iwave) * (mid - 1)) + mid
        out = list(' ' * width)
        if d.date() == plot.date():
            out = list('-' * width)
        out[mid] = ':'
        out[p] = '*' if p in {e, i} else 'p'
        out[e] = '*' if e in {i, p} else 'e'
        out[i] = '*' if i in {p, e} else 'i'
        print(d.strftime('%a %d %b'), ''.join(out))


if __name__ == '__main__':
    year = int(input('Enter your birth YEAR (0001-9999): '))
    month = int(input('Enter your birth MONTH (1-12): '))
    day = int(input('Enter your birth DAY (1-31): '))
    get_bio(birth=datetime(year, month, day))
    input('\nPress ENTER to Continue: ')
