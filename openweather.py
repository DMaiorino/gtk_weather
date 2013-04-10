#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import os.path
import ConfigParser
import sys
import argparse

class getWeather():

    def get_city_id(self, city):
    
        #city_list = ConfigParser.ConfigParser()
        #city_list.read('./city-id.txt')

        #try:
        #    city_id = city_list.get('CityList',city)
        #except:    
	    url = "http://openweathermap.org/data/2.0/find/name?q="+city+"&units=metric"

	    try:
		f = urllib2.urlopen(url)
	    except:
		print 'Error, unable to access http://openweathermap.org/data/2.0/find/name?q='+city 

	    json_data = f.read()
	    jdata_decoded = json.loads(json_data)
	    count = jdata_decoded['count']

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


    def get_json_data(self,city):
        
        city_id = self.get_city_id(city)
            
	if args.farenheight:
		url = "http://openweathermap.org/data/2.0/find/name?q="+city+"&units=imperial"
	else:
		url = "http://openweathermap.org/data/2.0/find/name?q="+city+"&units=metric"
        	#url = "http://openweathermap.org/data/2.0/weather/city/"+str(city_id)+"?type=json"
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

	w_data['id'] = str(jdata_decoded['list'][0]['id'])
        w_data['name'] = str(jdata_decoded['list'][0]['name'])
        w_data['date'] = str(jdata_decoded['list'][0]['date'])
        w_data['temp'] = str(jdata_decoded['list'][0]['main']['temp'])
	#print "What"+w_data['temp'] 
        w_data['pressure'] = str(jdata_decoded['list'][0]['main']['pressure'])
        w_data['humidity'] = str(jdata_decoded['list'][0]['main']['humidity'])+"%"
        w_data['wind'] = str(jdata_decoded['list'][0]['wind']['speed'])+" m/s"
        w_data['clouds'] = str(jdata_decoded['list'][0]['clouds']['all'])+" m/s"
        w_data['img'] = (jdata_decoded['list'][0]['weather'][0]['icon'])
        w_data['weather'] = str(jdata_decoded['list'][0]['weather'][0]['main'])
        
        w_iconname = w_data['img'] + ".png"

	#Pull icon name from site        
#        if not os.path.exists('./images/'+w_iconname):
#            w_icon = urllib2.urlopen(w_iconname).read()
#            #w_icon = urllib2.urlopen(w_img).read()
#            output = open('./images/'+w_iconname,'wb')
#            output.write(w_icon)
#            output.close()
         
        w_data['img'] = str(w_iconname)
        
        return w_data    
    
    def main(self, city):
        
        weather_data = self.get_weather(city)
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
    parser.add_argument("city", help="Search this city for weather information")
    parser.add_argument("-f","--farenheight", action="store_true", help="Set metics to Farenheight")
    parser.add_argument("-c","--celcius", action="store_true", help="Set metics to Celcius")
    args = parser.parse_args()
    #End option settings#

    app.main(str(args.city))
