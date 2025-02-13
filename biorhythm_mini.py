﻿#!/usr/bin/env python3
""" A minimalist Python module for generating a biorhythm chart.
https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)
History:
01.00 2025-Jan-01 Scott S. Initial release.
01.01 2025-Jan-20 Scott S. Added verbose mode.
01.02 2025-Feb-14 Scott S. Added header switch.

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

#!/usr/bin/env python3
# EXAMPLES FILE : Abraham Lincoln, day of the Gettysburg Address
#                 output optimized for a command window of 80x24 characters
from biorhythm_mini import get_bio
from datetime import datetime
birth, plot = datetime(1809, 2, 12), datetime(1863, 11, 19)
get_bio(birth=birth, plot=plot, width=45, days=7,
        header=True, verbose=False)
print('Outlook for Today:')
get_bio(birth=birth, plot=plot, width=45, days=0,
        header=False, verbose=True)
input('Press ENTER to Continue: ')

BIORHYTHM for Birth Date: Sunday, 12 February 1809
p=physical, e=emotional, i=intellectual for days since birth
-100% ================================= +100%
              i       :            p  e       Thu 12 Nov 1863, Day=19,996
                  i   :       p         e     Fri 13 Nov 1863, Day=19,997
                     i: p                 e   Sat 14 Nov 1863, Day=19,998
                   p  :  i                 e  Sun 15 Nov 1863, Day=19,999
             p        :      i            e   Mon 16 Nov 1863, Day=20,000
        p             :          i      e     Tue 17 Nov 1863, Day=20,001
    p                 :             i e       Wed 18 Nov 1863, Day=20,002
--p-------------------:------------e---i----- Thu 19 Nov 1863, Day=20,003
 p                    :        e         i    Fri 20 Nov 1863, Day=20,004
 p                    :   e               i   Sat 21 Nov 1863, Day=20,005
   p                  e                   i   Sun 22 Nov 1863, Day=20,006
      p          e    :                   i   Mon 23 Nov 1863, Day=20,007
           pe         :                  i    Tue 24 Nov 1863, Day=20,008
        e       p     :                 i     Wed 25 Nov 1863, Day=20,009
     e               p:              i        Thu 26 Nov 1863, Day=20,010
Outlook for Today:
--p-------------------:------------e---i----- Thu 19 Nov 1863, Day=20,003
                                              p:-94.2%  e:+62.3%  i:+81.5%
Press ENTER to Continue:

Please consider giving to cancer research.
https://braintumor.org/
https://www.cancer.org/
"""

from datetime import datetime as dt, timedelta as td
from math import floor, pi, sin


def get_bio(birth=dt.now(), plot=dt.now(), width=45, days=7,
            header=True, verbose=True):
    """ Plots a chart of physical, emotional, and intellectual cycles.
    PARAMETERS:
    birth   : birth date of the person
    plot    : plot date of the chart
    width   : width of the chart
    days    : number of days to show before and after the plot date
    header  : if true, include a header above the chart output
    verbose : if true, include the daily percentages with the chart output
    """
    pwave, ewave, iwave = 23, 28, 33  # physical, emotional, intellectual
    width = 15 if width < 15 else width  # minimum chart width
    midwidth = floor(width / 2)  # middle point of chart, distance to edge
    if header:
        print('BIORHYTHM for Birth Date:', birth.strftime('%A, %d %B %Y'))
        print('p=physical, e=emotional, i=intellectual for days since birth')
        print('-100%', '=' * (width - 12), '+100%')  # 12 for literals/spaces
    dates = (plot + td(days=d) for d in range(-days, days + 1))
    for d in dates:  # generator expression above yields dates lazily as used
        n = (d - birth).days  # number of days since birth
        # sine models -/+ percentages of distance from middle point of chart
        _p = sin(2 * pi * n / pwave)  # published formula calculations
        _e = sin(2 * pi * n / ewave)
        _i = sin(2 * pi * n / iwave)
        p = midwidth + floor(_p * (midwidth - 1))  # middle point to edges
        e = midwidth + floor(_e * (midwidth - 1))
        i = midwidth + floor(_i * (midwidth - 1))
        out = list(('-' if d.date() == plot.date() else ' ') * width)
        out[midwidth] = ':'
        out[p] = '*' if p in {e, i} else 'p'  # '*' for overlapping values
        out[e] = '*' if e in {i, p} else 'e'
        out[i] = '*' if i in {p, e} else 'i'
        print(''.join(out), d.strftime('%a %d %b %Y,'), 'Day={:,}'.format(n))
        if verbose:  # verbose outputs formatted percentages
            print(' ' * width,
                  f'p:{_p*100:+.1f}%  e:{_e*100:+.1f}%  i:{_i*100:+.1f}%')


if __name__ == '__main__':
    year = int(input('Enter your birth YEAR (0001-9999): '))
    month = int(input('Enter your birth MONTH (1-12): '))
    day = int(input('Enter your birth DAY (1-31): '))
    get_bio(birth=dt(year, month, day))
    input('\nPress ENTER to Continue: ')
