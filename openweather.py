#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import os.path
import ConfigParser
import sys

class getWeather():

    def get_city_id(self, city):
    
        city_list = ConfigParser.ConfigParser()
        city_list.read('./city-id.txt')

        try:
            city_id = city_list.get('CityList',city)
        except:    
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
	print "City_id is: " + str(city_id)
            
        url = "http://openweathermap.org/data/2.0/weather/city/"+str(city_id)+"?type=json"
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
        w_data['temp'] = str(jdata_decoded['main']['temp'] - 273.15)
        w_data['pressure'] = str(jdata_decoded['main']['pressure']*0.75)+" mmHg"
        w_data['humidity'] = str(jdata_decoded['main']['humidity'])+"%"
        w_data['wind'] = str(jdata_decoded['wind']['speed'])+" m/s"
        w_data['clouds'] = str(jdata_decoded['clouds']['all'])+"%"
        w_data['img'] = (jdata_decoded['weather'][0]['icon'])
        w_data['weather'] = (jdata_decoded['weather'][0]['main'])
        
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
        print 'Temperature :',weather_data['temp']+"C"
        print 'Pressure    :',weather_data['pressure']
        print 'Humidity    :',weather_data['humidity']
        print 'Wind        :',weather_data['wind']
        print 'Clouds      :',weather_data['clouds']
        print 'Currently   :',weather_data['weather']
        

if __name__ == "__main__":

    app = getWeather()
    app.main(str(sys.argv[1]))
