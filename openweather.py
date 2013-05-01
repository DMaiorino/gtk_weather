#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import ConfigParser
import json
import os.path
import sys
import urllib2

class getWeather():

    def get_city_id(self, city):
    
        city_list = ConfigParser.ConfigParser()
	url = "http://openweathermap.org/data/2.0/find/name?q="+city+"&units=metric"
	
	if args.default:
		city_list.read('./config.ini')
		try:
			city_id = city_list.get('default city','city_id')
		except:
			print 'Error, unable to load city_id from configuration'
			sys.exit()
		return city_id

	try:
		f = urllib2.urlopen(url)
	except:
		print 'Error, unable to access http://openweathermap.org/data/2.0/find/name?q='+city 
		sys.exit()
	
	json_data = f.read()
	jdata_decoded = json.loads(json_data)
	
	#Check if data has been provided
	try: 
		count = jdata_decoded['count']
	except:
		print "No information could be found for provided city, exiting..."
		sys.exit()

	if ( count > 1 ):
		print 'More then one site returned, please select from the following:'	
		counter = 0
		while (counter < count):
			city_id = jdata_decoded['list'][counter]['id']
			country = jdata_decoded['list'][counter]['sys']['country']
			print "["+str(counter)+"] " + "City: "+city+", Country: "+country+ "  ("+str(city_id)+")"
			counter = counter + 1
		user_selection = input("Please choose a number: ")
		if 0 <= user_selection < count:
			return jdata_decoded['list'][user_selection]['id']
		else:
			print 'Error: '+str(user_selection)+' not a valid option, exiting...'
			sys.exit()
	elif count == 1 :
		return jdata_decoded['list'][0]['id']
	else:
		print "No information found for provided site. Exiting"
		sys.exit()



    def get_json_data(self,city):
        
        city_id = self.get_city_id(city)
            
	if args.farenheight:
		url = "http://openweathermap.org/data/2.0/weather/city/"+str(city_id)+"?type=json&units=imperial"
	else:
		url = "http://openweathermap.org/data/2.0/weather/city/"+str(city_id)+"?type=json&units=metric"
        try:
            f = urllib2.urlopen(url)
        except:
            return None
        s = f.read()           
        return s

        
    def get_weather(self, city):
        
        json_data = self.get_json_data(city)
        jdata_decoded = json.loads(json_data)
        w_data = {}

	w_data['id'] = str(jdata_decoded['id'])
        w_data['name'] = str(jdata_decoded['name'])
        w_data['date'] = str(jdata_decoded['date'])
        w_data['temp'] = str(jdata_decoded['main']['temp'])
        w_data['pressure'] = str(jdata_decoded['main']['pressure'])
        w_data['humidity'] = str(jdata_decoded['main']['humidity'])+"%"
        w_data['wind'] = str(jdata_decoded['wind']['speed'])+" m/s"
        w_data['clouds'] = str(jdata_decoded['clouds']['all'])+" m/s"
        w_data['img'] = (jdata_decoded['weather'][0]['icon'])
        w_data['weather'] = str(jdata_decoded['weather'][0]['main'])
       
        return w_data    

    def check_args(self):
	if args.default and args.city:
		print 'Error: unable to lookup city when using default option'
		sys.exit()
	if not args.city and not args.default:
		print 'Error: too few arguments'
		sys.exit()

    
    def main(self, city):
        
        weather_data = self.get_weather(city)
	if args.city:
		print 'Weather in '+city+''
	else:
		print 'Weather in '+city+''

	if args.farenheight:
		print 'Temperature :',weather_data['temp']+ " F"
	else:
		print 'Temperature :',weather_data['temp']+ " C"
        print 'Pressure    :',weather_data['pressure']
        print 'Humidity    :',weather_data['humidity']
        print 'Wind        :',weather_data['wind']
        print 'Clouds      :',weather_data['clouds']
        print 'Currently   :',weather_data['weather']
        

if __name__ == "__main__":

    app = getWeather()

    #Start option settings#
    parser = argparse.ArgumentParser()
    parser.add_argument("city", nargs='?', help="Search this city for weather information")
    parser.add_argument("-f","--farenheight", action="store_true", help="Set metics to Farenheight")
    parser.add_argument("-c","--celcius", action="store_true", help="Set metics to Celcius")
    parser.add_argument("-d","--default", action="store_true", help="Weather for default city")
    args = parser.parse_args()
    app.check_args()
    #End option settings#

    app.main(str(args.city))
