#!/usr/bin/env python3
""" A super simple Python module for generating a biorhythm chart.
(horizontal layout version)

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
from datetime import date, timedelta
from math import pi, sin


def get_bio(birth=date.today(), plot=date.today(), rows=21, days=7):
    """ Plots a chart of physical, emotional, and intellectual cycles.
    PARAMETERS:
    birth : birth date of the person
    plot  : plot date of the chart
    rows  : number of rows to show for the chart height
    days  : number of days to show before and after the plot date
    """
    rows = (rows + 1) if (rows % 2) == 0 else rows  # force odd rows
    midrow = rows // 2
    print('BIORHYTHM for Birth Date:', f'{birth:%A, %d %B %Y}')
    print('               Plot Date:', f'{plot:%A, %d %B %Y}')
    print('p=physical, e=emotional, i=intellectual for days since birth')
    data = []
    dates = (plot + timedelta(days=d) for d in range(-days, days + 1))
    for d in dates:
        n = (d - birth).days  # number of days since birth
        p = sin(2 * pi * n / 23)  # physical
        e = sin(2 * pi * n / 28)  # emotional
        i = sin(2 * pi * n / 33)  # intellectual
        data.append((d.day, p, e, i))  # extra parentheses, appends tuple
    for row in range(rows):
        label = '     '  # labels use 5 chars
        if row == 0:
            label = '+100%'
        elif row == midrow:
            label = '    0'
        elif row == (rows - 1):
            label = '-100%'
        out = ''
        for day, p, e, i in data:
            symbol = '   '  # symbols use 3 chars
            if (midrow - int(p * midrow)) == row:
                symbol = ' p ' if symbol == '   ' else ' * '
            if (midrow - int(e * midrow)) == row:
                symbol = ' e ' if symbol == '   ' else ' * '
            if (midrow - int(i * midrow)) == row:
                symbol = ' i ' if symbol == '   ' else ' * '
            if day == plot.day:
                symbol = ' : ' if symbol == '   ' else symbol
            if midrow == row:
                symbol = ' - ' if symbol == '   ' else symbol
            out += symbol
        print(label, out, sep=' |')
    print('     ', '---' * (days * 2 + 1), sep=' +')
    out = ''
    for day, *_ in data:
        out += f'{day:^3}'
    print('  Day', out, sep='  ')


if __name__ == '__main__':
    year = int(input('Enter your birth YEAR (0001-9999): '))
    month = int(input('Enter your birth MONTH (1-12): '))
    day = int(input('Enter your birth DAY (1-31): '))
    get_bio(birth=date(year, month, day))
    input('Press ENTER to Continue: ')
