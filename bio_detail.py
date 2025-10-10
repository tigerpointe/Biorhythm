#!/usr/bin/env python3
""" A Python module for generating a detailed biorhythm chart.

BIORHYTHM for Birth Date: Sunday, 12 February 1809
p=physical, e=emotional, i=intellectual for days since birth
Date            -100% ============= +100%    p       e       i    Day
Thu 12 Nov 1863         i   :     p e      +63.1%  +78.2%  -37.2% 19,996
Fri 13 Nov 1863           i :   p    e     +39.8%  +90.1%  -18.9% 19,997
Sat 14 Nov 1863             ip        e    +13.6%  +97.5%   -0.0% 19,998
Sun 15 Nov 1863            p: i        e   -13.6% +100.0%  +18.9% 19,999
Mon 16 Nov 1863         p   :   i     e    -39.8%  +97.5%  +37.2% 20,000
Tue 17 Nov 1863       p     :    i   e     -63.1%  +90.1%  +54.1% 20,001
Wed 18 Nov 1863     p       :      ie      -81.7%  +78.2%  +69.0% 20,002
Thu 19 Nov 1863 --p---------:-----e-i----  -94.2%  +62.3%  +81.5% 20,003
Fri 20 Nov 1863   p         :   e     i    -99.8%  +43.4%  +91.0% 20,004
Sat 21 Nov 1863   p         : e       i    -97.9%  +22.3%  +97.2% 20,005
Sun 22 Nov 1863    p        e         i    -88.8%   +0.0%  +99.9% 20,006
Mon 23 Nov 1863     p     e :         i    -73.1%  -22.3%  +99.0% 20,007
Tue 24 Nov 1863        pe   :         i    -52.0%  -43.4%  +94.5% 20,008
Wed 25 Nov 1863       e   p :        i     -27.0%  -62.3%  +86.6% 20,009
Thu 26 Nov 1863     e       p       i       -0.0%  -78.2%  +75.6% 20,010

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
from datetime import date, timedelta
from math import pi, sin


def get_data(birth=date.today(), plot=date.today(), days=7):
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


def plot_chart(birth=date.today(), plot=date.today(), width=25, days=7):
    """ Plots a chart of physical, emotional, and intellectual cycles.
    PARAMETERS:
    birth : birth date of the person
    plot  : plot date of the chart
    width : width of the chart in characters
    days  : number of days to show before and after the plot date
    REMARKS:
    The output is optimized for a traditional 80x24 console window.
    The chart width and days range can be set to fit your system.
    """
    width = max(15, width)
    midwidth = width // 2
    print('BIORHYTHM for Birth Date:', f'{birth:%A, %d %B %Y}')
    print('p=physical, e=emotional, i=intellectual for days since birth')
    print('Date', ' ' * 10, '-100%', '=' * (width - 12), '+100%',
          '   p   ', '   e   ', '   i   ', 'Day')
    data = get_data(birth=birth, plot=plot, days=days)
    for d, n, p, e, i in data:
        _p = midwidth + int(p * (midwidth - 1))  # starting from middle zero,
        _e = midwidth + int(e * (midwidth - 1))  # adds -/+ percentages of
        _i = midwidth + int(i * (midwidth - 1))  # width toward -100% or +100%
        out = ['-' if d == plot else ' '] * width
        out[midwidth] = ':'
        out[_p] = '*' if _p in {_e, _i} else 'p'  # '*' for overlapping values
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
    plot_chart(birth=date(year, month, day), width=width, days=days)
    input('Press ENTER to Continue: ')
