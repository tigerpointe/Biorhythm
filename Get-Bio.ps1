<#

.SYNOPSIS
A PowerShell script for generating a biorhythm chart.

Please consider giving to cancer research.

.DESCRIPTION
Plots a chart of physical, emotional and intellectual cycles.

.PARAMETER birthDate
Specifies the birth date of the person.

.PARAMETER plotDate
Specifies the plot date of the chart.

.PARAMETER width
Specifies the width of the chart.

.PARAMETER days
Specifies the number of days to plot.

.INPUTS
None.

.OUTPUTS
A biorhythm chart.

.EXAMPLE 
.\Get-Bio.ps1 -birthDate (Get-Date -Year 1908 -Month 9 -Day 15)
Gets a biorhythm chart for the specified birth date.

.NOTES
MIT License

Copyright (c) 2022 TigerPointe Software, LLC

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

Create a custom Get-Bio.bat file for your own birthday or favorite celebrity.

@echo off
: Penny Singleton was an American actress and labor
: leader.  During her 60-year career on stage, screen,
: radio and television, Singleton appeared as the
: comic-strip heroine Blondie Bumstead in a series of
: 28 motion pictures from 1938 until 1950 and the
: popular Blondie radio program from 1939 until 1950.
: Singleton also provided the voice of Jane Jetson in
: the animated series The Jetsons from 1962 to 1963.
: https://en.wikipedia.org/wiki/Penny_Singleton
set cmd="& '.\Get-Bio.ps1' (Get-Date -Year 1908 -Month 9 -Day 15)"
PowerShell.exe -Command %cmd%
echo.
pause

If you enjoy this software, please do something kind for free.

History:
01.00 2022-Dec-12 Scott S. Initial release.
01.01 2022-Dec-15 Scott S. Added the plot date to the chart header.
01.02 2023-Jun-21 Scott S. Optimized the source code and comments.

.LINK
https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)

.LINK
https://braintumor.org/

.LINK
https://www.cancer.org/

#>

# Gets a biorhythm chart.
param
(
    $birthDate = (Get-Date) # today
  , $plotDate  = (Get-Date) # today
  , $width = 50             # 50 characters
  , $days  = 29             # 29 days
)

# Define the output date formats
$longDate  = "ddd MMM dd yyyy"; # Wed Jan 31 1900
$shortDate = "ddd MMM dd";      # Wed Jan 31

# Define the wavelengths (days per cycle)
# https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)
$pWave = 23; # physical
$eWave = 28; # emotional
$iWave = 33; # intellectual

# Sanity check (minimum width of the chart title)
if ($width -lt 12) { $width = 12; }

# Calculate the midpoints of the chart
$midWidth = [Math]::Floor($width / 2);
$midDays  = [Math]::Floor($days  / 2);

# Count the number of days since birth
$count = (New-TimeSpan -Start $birthDate.Date `
                       -End   $plotDate.Date).Days;

# Write the chart header and label keys
Write-Output "Birth:  $($birthDate.ToString($longDate))";
Write-Output "Plot:   $($plotDate.ToString($longDate))";
Write-Output "Alive:  $($count.ToString("N0")) days";
Write-Output "p:      Physical";
Write-Output "e:      Emotional";
Write-Output "i:      Intellectual";

# Write the chart title
# The length of "-100% " and " +100%" equals 12 characters total
$title = "PASSIVE  CRITICAL  ACTIVE";
$pad   = $shortDate.Length + 1 + $midWidth;       # chart center
$pad   = $pad - [Math]::Floor($title.Length / 2); # title center
Write-Output "$(" " * $pad)$title".PadRight($shortDate.Length + 1 + $width);
Write-Output "$(" " * $shortDate.Length) -100% $("=" * ($width - 12)) +100%";

# Calculate the lowest date of the chart
$lowDate = $plotDate.AddDays(-$midDays);

# Loop through each of the days
for ($n = 0; $n -lt $days; $n++)
{

  # Calculate the next day to plot
  $nextDate = $lowDate.AddDays($n);

  # Count the number of days since birth
  $count = (New-TimeSpan -Start $birthDate.Date `
                         -End   $nextDate.Date).Days;
  
  # Calculate the point values
  # https://en.wikipedia.org/wiki/Biorhythm_(pseudoscience)#Calculation
  # Sine oscillates between -1 and +1 as increasing radian values are
  # passed; the angle value is calculated using 2*PI, which is the
  # number of radians in a circle; the official calculation specifies to
  # then multiply by the number of days since birth and divide by the
  # wavelength; the resulting amplitude will be a decimal value which
  # occurs somewhere between -1 and +1
  $pValue = [Math]::Sin((2 * [Math]::PI * $count) / $pWave);
  $eValue = [Math]::Sin((2 * [Math]::PI * $count) / $eWave);
  $iValue = [Math]::Sin((2 * [Math]::PI * $count) / $iWave);

  # Calculate the point locations
  # The point values must be multiplied by half of the chart width to
  # calculate the final -/+ distance from the center line
  $pIndex = [Math]::Floor($pValue * ($midWidth - 1)) + $midWidth;
  $eIndex = [Math]::Floor($eValue * ($midWidth - 1)) + $midWidth;
  $iIndex = [Math]::Floor($iValue * ($midWidth - 1)) + $midWidth;

  # Write the plot line, use an array of spaces equal to the chart width
  $space = " ";
  if ($nextDate -eq $plotDate) { $space = "-"; }
  $out = ($space * $width).ToCharArray();
  $out[$midWidth] = ":";
  $out[$pIndex]   = "p";
  $out[$eIndex]   = "e";
  $out[$iIndex]   = "i";
  if ($pIndex -eq $eIndex) { $out[$pIndex] = "*"; }
  if ($eIndex -eq $iIndex) { $out[$eIndex] = "*"; }
  if ($iIndex -eq $pIndex) { $out[$iIndex] = "*"; }
  Write-Output "$($nextDate.ToString($shortDate)) $([String]::new($out))";

}