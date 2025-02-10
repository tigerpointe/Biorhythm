#!/usr/bin/env python3
# EXAMPLES FILE : Abraham Lincoln, day of the Gettysburg Address
#                 output optimized for a command window of 80x24 characters
from biorhythm_mini import get_bio
from datetime import datetime
birth = datetime(1969, 7, 5)
get_bio(birth=birth, width=45, days=7,
        header=True, verbose=False)
print('Outlook for Today:')
get_bio(birth=birth, width=45, days=0,
        header=False, verbose=True)
input('Press ENTER to Continue: ')