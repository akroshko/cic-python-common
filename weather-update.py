#!/usr/bin/env python
# -*- coding: utf-8 -*-
import lxml.html
import urllib
url = "http://wxdata.weather.com/wxdata/weather/local/CAXX0442?cc=*&unit=m&dayf=3"
uh = urllib.urlopen(url)
html = lxml.html.parse(uh)
# get out the good data
location=html.xpath('//loc/dnam/text()')[0]
sunrise=html.xpath('//loc/sunr/text()')[0]
sunset=html.xpath('//loc/suns/text()')[0]
print location + " Sunrise: %s Sunset: %s" % (sunrise.replace(' ','').lower(),sunset.replace(' ','').lower())
temp=html.xpath('//cc/tmp/text()')[0]
humid=html.xpath('//cc/hmid/text()')[0]
cond=html.xpath('//cc//t/text()')[0]
wind=html.xpath('//cc/wind/s/text()')[0]
winddir=html.xpath('//cc/wind/t/text()')[0]
print " %s %s°C with Humidity %s%% Wind: %skm/h %s" % (cond,temp,humid,wind,winddir)
dayhi = html.xpath('//dayf/day/hi/text()')[0]
daylo = html.xpath('//dayf/day/low/text()')[0]
daycond = html.xpath('//dayf/day/part/t/text()')[0]
dayfhi = html.xpath('//dayf/day/hi/text()')[1]
dayflo = html.xpath('//dayf/day/low/text()')[1]
dayfcond = html.xpath('//dayf/day/part/t/text()')[1]
day2hi = html.xpath('//dayf/day/hi/text()')[2]
day2lo = html.xpath('//dayf/day/low/text()')[2]
day2cond = html.xpath('//dayf/day/part/t/text()')[2]
print " Today Hi/Lo: %s %s°C/%s°C" % (daycond, dayhi, daylo)
print " Tomorrow Hi/Lo: %s %s°C/%s°C" % (dayfcond,dayfhi,dayflo)
print " Day after Tomorrow Hi/Lo: %s %s°C/%s°C"  % (day2cond,day2hi,day2lo)
