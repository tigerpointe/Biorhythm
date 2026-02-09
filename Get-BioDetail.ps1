#!/usr/bin/env pwsh

<#
.SYNOPSIS
Gets a detailed biorhythm.

.DESCRIPTION
A PowerShell module for generating a detailed biorhythm chart.

BIORHYTHM for Birth Date: Sunday, 12 February 1809
p=physical, e=emotional, i=intellectual for days since birth
  Date            -100% ========= +100%    p       e       i    Day
  Thu 12 Nov 1863        i  :    p e     +63.1%  +78.2%  -37.2% 19,996
  Fri 13 Nov 1863          i:  p    e    +39.8%  +90.1%  -18.9% 19,997
  Sat 14 Nov 1863           ip      e    +13.6%  +97.5%   -0.0% 19,998
  Sun 15 Nov 1863          p:i       e   -13.6% +100.0%  +18.9% 19,999
  Mon 16 Nov 1863        p  :  i    e    -39.8%  +97.5%  +37.2% 20,000
  Tue 17 Nov 1863      p    :   i   e    -63.1%  +90.1%  +54.1% 20,001
  Wed 18 Nov 1863    p      :     ie     -81.7%  +78.2%  +69.0% 20,002
> Thu 19 Nov 1863 --p-------:----e-i---  -94.2%  +62.3%  +81.5% 20,003
  Fri 20 Nov 1863   p       :  e    i    -99.8%  +43.4%  +91.0% 20,004
  Sat 21 Nov 1863   p       : e     i    -97.9%  +22.3%  +97.2% 20,005
  Sun 22 Nov 1863    p      e       i    -88.8%   +0.0%  +99.9% 20,006
  Mon 23 Nov 1863     p   e :       i    -73.1%  -22.3%  +99.0% 20,007
  Tue 24 Nov 1863       pe  :       i    -52.0%  -43.4%  +94.5% 20,008
  Wed 25 Nov 1863      e  p :      i     -27.0%  -62.3%  +86.6% 20,009
  Thu 26 Nov 1863    e      p     i       -0.0%  -78.2%  +75.6% 20,010

.INPUTS
None, nothing is read from the pipeline

.OUTPUTS
The chart text content

.NOTES
MIT License

Copyright (c) 2026 TigerPointe Software, LLC

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

.LINK
https://braintumor.org/

.LINK
https://www.cancer.org/
#>


<#
.SYNOPSIS
Gets the data.

.DESCRIPTION
Gets the calculated physical, emotional, and intellectual data.

.PARAMETER Birth
birth date of the person

.PARAMETER Plot
plot date of the data

.PARAMETER Days
number of days to include before and after the plot date

.INPUTS
None, nothing is read from the pipeline

.OUTPUTS
The physical, emotional, and intellectual data
#>
function Get-Data {
  param (
    $Birth = (Get-Date).Date
    , $Plot = (Get-Date).Date
    , $Days = 7
  )
  $data = @()
  for ($d = $Plot.AddDays(-$Days); `
      $d -le $Plot.AddDays($Days); `
      $d = $d.AddDays(1)) {
    $n = ($d.Date - $Birth.Date).Days  # number of days since birth
    $p = [Math]::Sin(2 * [Math]::PI * $n / 23)  # physical
    $e = [Math]::Sin(2 * [Math]::PI * $n / 28)  # emotional
    $i = [Math]::Sin(2 * [Math]::PI * $n / 33)  # intellectual
    $data += @{
      d = $d
      n = $n
      p = $p
      e = $e
      i = $i
    }  # appends hashtable object
  }
  return $data
}


<#
.SYNOPSIS
Builds the chart.

.DESCRIPTION
Plots a chart of physical, emotional, and intellectual cycles.

.PARAMETER Birth
birth date of the person

.PARAMETER Plot
plot date of the chart

.PARAMETER Width
width of the chart in characters

.PARAMETER Days
number of days to show before and after the plot date

.INPUTS
None, nothing is read from the pipeline

.OUTPUTS
The chart text content

.NOTES
The default output is optimized for a traditional 80x24 console window.
The chart width and days range can be set to fit your system.
#>
function Build-Chart {
  param (
    $Birth = (Get-Date).Date
    , $Plot = (Get-Date).Date
    , $Width = 25
    , $Days = 7
  )
  $Width = [Math]::Max(15, $Width)
  $midwidth = [Math]::Truncate($Width / 2)
  "BIORHYTHM for Birth Date: {0:dddd, dd MMMM yyyy}" -f $Birth
  "p=physical, e=emotional, i=intellectual for days since birth"
  "  Date            -100% {0} +100%    p       e       i    Day" `
    -f ("=" * ($Width - 12))
  $data = Get-Data -Birth $Birth `
    -Plot $Plot `
    -Days $Days
  foreach ($row in $data) {
    # from middle zero, adds -/+ percentages of width toward -100% or +100%
    $p = $midwidth + [Math]::Truncate($row.p * ($midwidth - 1))
    $e = $midwidth + [Math]::Truncate($row.e * ($midwidth - 1))
    $i = $midwidth + [Math]::Truncate($row.i * ($midwidth - 1))
    $space = " "
    $pointer = " "
    if ($row.d.Date -eq $Plot.Date) {
      $space = "-"
      $pointer = ">"
    }
    $out = ($space * $Width).ToCharArray()
    $out[$midwidth] = ":"
    $out[$p] = "p"
    $out[$e] = "e"
    $out[$i] = "i"
    # '*' for overlapping values
    if ($p -in @($e, $i)) { $out[$p] = "*" }
    if ($e -in @($i, $p)) { $out[$e] = "*" }
    if ($i -in @($p, $e)) { $out[$i] = "*" }
    # columns 3, 4, and 5 use fixed column widths with -/+ signs
    ("{0} {1:ddd dd MMM yyyy} {2} " + `
      "{3,7:+0.0%;-0.0%} {4,7:+0.0%;-0.0%} {5,7:+0.0%;-0.0%} {6:N0}") `
      -f $pointer, $row.d, ($out -join ""), $row.p, $row.e, $row.i, $row.n
  }
}


if (($MyInvocation.InvocationName -match "\.ps1$") -or `
  ($MyInvocation.InvocationName -eq ".")) {
  try {
    [int]$year = Read-Host -Prompt "Enter your birth YEAR (0001-9999)"
    [int]$month = Read-Host -Prompt "Enter your birth MONTH (1-12)"
    [int]$day = Read-Host -Prompt "Enter your birth DAY (1-31)"
    $width = 25
    $tmp = Read-Host -Prompt "Enter the chart WIDTH (default=$width)"
    if (-not [String]::IsNullOrWhiteSpace($tmp)) { [int]$width = $tmp }
    $days = 7
    $tmp = Read-Host -Prompt "Enter the before/after DAYS (default=$days)"
    if (-not [String]::IsNullOrWhiteSpace($tmp)) { [int]$days = $tmp }
    $birth = Get-Date -Year $year `
      -Month $month `
      -Day $day
    Build-Chart -Birth $birth `
      -Width $width `
      -Days $days
  }
  catch {
    Write-Error -Message $_.Exception.Message
  }
  finally {
    Read-Host -Prompt "Press ENTER to Continue"
  }
}
