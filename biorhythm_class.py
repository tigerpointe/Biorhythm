#!/usr/bin/env python3
""" A Python module for generating a biorhythm chart (Class Version).
https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)

History:
01.00 2025-Apr-15 Scott S. Initial release.
01.01 2025-May-04 Scott S. Code optimizations.
01.02 2025-May-26 Scott S. Chart layout, magic methods.

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

Create a custom script to generate an entire year of biorhythms.

#!/usr/bin/env python3
from biorhythm_class import Biorhythm
year = int(input('Enter your birth YEAR (0001-9999): '))
month = int(input('Enter your birth MONTH (1-12): '))
day = int(input('Enter your birth DAY (1-31): '))
Biorhythm.from_ymd(year, month, day).write_year()
input('Press ENTER to Continue: ')

If you enjoy this software, please do something kind for free.

Please consider giving to cancer research.
https://braintumor.org/
https://www.cancer.org/
"""
from datetime import datetime, timedelta
from math import floor, pi, sin
import sys


class Biorhythm:
    """ A class for generating a biorhythm chart."""

    pwave, ewave, iwave = 23, 28, 33  # physical, emotional, intellectual

    def __init__(self, birth=datetime.now()):
        """ Initializes a chart.
        PARAMETERS:
        birth : birth date of the person
        """
        self.birth = birth

    def __calculate(self, n):
        """ Calculates the published formula values.
        PARAMETERS:
        n : number of days since birth
        RETURNS:
        The physical, emotional, intellectual, and average values
        """
        # sine models -/+ percentages of distance from middle point of chart
        p = sin(2 * pi * n / Biorhythm.pwave)  # physical
        e = sin(2 * pi * n / Biorhythm.ewave)  # emotional
        i = sin(2 * pi * n / Biorhythm.iwave)  # intellectual
        a = (p + e + i) / 3  # average
        return p, e, i, a

    def __get_detail(self, d):
        """ Gets the percentage details for a date.
        PARAMETERS:
        d : date for which to get the percentage details
        RETURNS:
        The percentage details
        """
        n = (d - self.birth).days  # number of days since birth
        p, e, i, a = self.__calculate(n=n)  # percentage values
        return f'p:{p:+.1%}, e:{e:+.1%}, i:{i:+.1%}, a:{a:+.1%}'

    def __plot(self, plot, width, days, detail, file, flush):
        """ Plots a chart of physical, emotional, and intellectual cycles.
        PARAMETERS:
        plot   : plot date of the chart
        width  : width of the chart in characters
        days   : number of days to show before and after the plot date
        detail : if true, show the percentage details for the plot date
        file   : object with a write method, such as the console or a file
        flush  : if true, commit the file output immediately without buffering
        """
        width = 25 if width < 25 else width  # minimum width of chart
        midwidth = floor(width / 2)  # middle point of chart, distance to edge
        print('BIORHYTHM for Birth Date:', f'{self.birth:%A, %d %B %Y}',
              file=file, flush=flush)
        print('p=physical, e=emotional, i=intellectual, a=average',
              'for days since birth',
              file=file, flush=flush)
        print(f'{"    ": <15}',  # left-justify date width
              f'{"PASSIVE  CRITICAL  ACTIVE": ^{width}}',  # center over chart
              f'{"   ": >10}',  # right-justify day width
              file=file, flush=flush)
        print(f'{"Date": <15}',  # left-justify date width
              f'-100% {"=" * (width - 12)} +100%',  # 12 for literals/spaces
              f'{"Day": >10}',  # right-justify day width
              file=file, flush=flush)
        dates = (plot + timedelta(days=d) for d in range(-days, days + 1))
        for d in dates:  # generator expression above yields dates lazily
            n = (d - self.birth).days  # number of days since birth
            _p, _e, _i, _a = self.__calculate(n=n)  # percentage values
            p = midwidth + floor(_p * (midwidth - 1))  # middle point to edges
            e = midwidth + floor(_e * (midwidth - 1))
            i = midwidth + floor(_i * (midwidth - 1))
            a = midwidth + floor(_a * (midwidth - 1))
            out = list(('-' if d.date() == plot.date() else ' ') * width)
            out[midwidth] = ':'
            out[p] = '*' if p in {e, i, a} else 'p'  # '*' for overlap values
            out[e] = '*' if e in {i, a, p} else 'e'
            out[i] = '*' if i in {a, p, e} else 'i'
            out[a] = '*' if a in {p, e, i} else 'a'
            print(f'{d:%a %d %b %Y}',  # formatted date
                  ''.join(out),  # chart output
                  f'{n: >10,}',  # right-justify day width, commas
                  file=file, flush=flush)
        if detail:  # detail outputs percentages for plot date
            out = self.__get_detail(d=plot)
            if len(out) <= width:  # check for fit
                print(f'{"Outlook Today": >15}',  # right-justify date width
                      f'{out: ^{width}}',  # center under chart
                      f'{"   ": >10}',  # right-justify day width
                      file=file, flush=flush)

    def __repr__(self):
        """ Returns a formal string representation."""
        return f'{type(self).__name__}(birth={self.birth.__repr__()})'

    def __str__(self):
        """ Returns an informal string representation."""
        return f'{self.birth.__str__()} {self.__get_detail(d=datetime.now())}'

    @classmethod
    def from_ymd(cls, year=datetime.now().year, month=datetime.now().month,
                 day=datetime.now().day):
        """ Initializes a chart from the year, month, and day.
        PARAMETERS:
        year  : birth year of the person
        month : birth month of the person
        day   : birth day of the person
        RETURNS:
        An instance of the class
        """
        return cls(birth=datetime(year, month, day))

    def print(self, plot=datetime.now(), width=45, days=14):
        """ Prints a chart to the console.
        PARAMETERS:
        plot  : plot date of the chart
        width : width of the chart in characters
        days  : number of days to show before and after the plot date
        """
        self.__plot(plot=plot, width=width, days=days, detail=True,
                    file=sys.stdout, flush=False)

    def write(self, plot=datetime.now(), width=45, days=14, echo=False):
        """ Writes a chart to a file.
        PARAMETERS:
        plot  : plot date of the chart
        width : width of the chart in characters
        days  : number of days to show before and after the plot date
        echo  : if true, echo the file content to the console
        RETURNS:
        The file name of the chart
        """
        filename = f'{self.birth:mybio.%Y.%m.%d.txt}'
        with open(filename, 'w') as file:
            self.__plot(plot=plot, width=width, days=days, detail=True,
                        file=file, flush=False)
        if echo:  # echo outputs file content to console
            with open(filename, 'r') as file:
                for line in file:
                    print(line, end='')  # read lines already end with '\n'
        print('BIORHYTHM saved to file:', filename)
        return filename

    def write_year(self, year=datetime.now().year, width=45):
        """ Writes an entire year of charts to monthly files.
        PARAMETERS:
        year  : plot year for the charts
        width : width of the charts in characters
        """
        for month in range(1, 13):  # for months 1 to 12
            plot = datetime(year, month, 15)  # middle day of month
            filename = f'{plot:%Y.%m.mybio.txt}'
            with open(filename, 'w') as file:
                print((f'{plot:%B %Y} ').upper(), end='',  # extra header
                      file=file, flush=False)
                self.__plot(plot=plot, width=width, days=21, detail=False,
                            file=file, flush=False)
            print('Saved:', filename)


if __name__ == '__main__':
    year = int(input('Enter your birth YEAR (0001-9999): '))
    month = int(input('Enter your birth MONTH (1-12): '))
    day = int(input('Enter your birth DAY (1-31): '))
    bio = Biorhythm(birth=datetime(year, month, day))
    answer = ''
    while answer not in {'y', 'n'}:
        answer = input('Save to file? (Y|N): ').lower()
    if answer == 'y':
        bio.write(echo=True)
    else:
        bio.print()
    input('Press ENTER to Continue: ')
