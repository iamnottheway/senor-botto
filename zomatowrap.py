
# zomato wrap : Zomato wrap is an api wrapper.

import requests

credentials = {
                # zomato api key to access taco resturant data
                "API_KEY":"e2a77aab96b73139c0d6c992dc0ba9ce"
}

class ZomatoApi():

    def __init__(self,API_KEY):
        self.API_KEY = API_KEY
        self.base_url = "https://developers.zomato.com/api/v2.1/"
        # the api key is passed in the header of the url
        self.headers = {"user-key":"{}".format(self.API_KEY)}

    def GetCategories(self):
        self.cat_url = self.base_url + "categories"
        #send a GET request
        self.response = requests.get(self.cat_url,headers=self.headers)
        return self.response.json()

    def GetCityDetails(self,location=None,coords=[None,None],max_count=5):
        """
            location    : location name
            coords      : [lat,lon] takes a list -----> optional
            max_count   : number of results to be displayed
        """
        self.location = location
        self.coords = coords
        self.max_count = max_count
        # api request url for cities
        self.city_url = self.base_url + "cities"

        if self.location == None and self.coords == None:
            return "\nError! Both can't be None\n"

        if self.location is None:
            self.params = {
                "count": "{}".format(self.max_count),
                "lat"  : "{}".format(self.coords[0]),
                "lon"  : "{}".format(self.coords[1])
            }
        else:
            self.params = {
                "q" : "{}".format(self.location),
                "count": "{}".format(self.max_count),
            }
        self.response = requests.get(self.city_url,headers=self.headers,params=self.params)
        return self.response.json()

    def GetResturantCollections(self,city_id = 280,max_count = 5):
        # get the ciy_id using GetCityDetails() method. It's tagged as 'id'
        self.city_id, self.max_count = city_id,max_count
        # resturant collection url
        self.res_url = self.base_url + "collections"
        if self.city_id == None and self.max_count == None:
            return "Error! city_id and max_count can't be None"

        self.params = {
            "city_id":"{}".format(self.city_id),
            "count"  :"{}".format(self.max_count)
        }
        self.response = requests.get(self.res_url,headers=self.headers,params=self.params)
        return self.response.json()

    def GetCuisines(self,city_id = 280,max_count = 5):
        self.city_id, self.max_count = city_id,max_count
        # resturant collection url
        self.cuisine_url = self.base_url + "cuisines"
        if self.city_id == None and self.max_count == None:
            return "Error! city_id and max_count can't be None"

        self.params = {
            "city_id":"{}".format(self.city_id),
            "count"  :"{}".format(self.max_count)
        }
        self.response = requests.get(self.cuisine_url,headers=self.headers,params=self.params)
        return self.response.json()


    def GetRestaurantTypes(self,city_id = 280):
        self.ResType = self.base_url + "establishments"
        self.city_id = city_id
        if self.city_id is None:
            return "Error! Can't be None"

        self.params = {
            'city_id':"{}".format(self.city_id)
        }
        self.response = requests.get(self.ResType,headers=self.headers,params=self.params)
        return self.response.json()

    def GetLocationUsingCoords(self,coords = [None,None]):
        self.coords = coords
        self.coord_url = self.base_url + "geocode"

        if self.coords is None:
            return "Error! coords takes a list"
        self.params = {
            'lat':"{}".format(self.coords[0]),
            'lon':"{}".format(self.coords[1])
        }
        self.response = requests.get(self.coord_url,headers=self.headers,params=self.params)
        return self.response.json()


    def GetLocations(self,q = "London",max_count = 5):
        self.q = q # query string
        self.max_count = max_count
        self.loc_url = self.base_url + "location"

        if self.coords is None:
            return "Error! Location cannot be None"

        self.params = {
            'q'     :"{}".format(self.q),
            'count' :"{}".format(self.max_count)
        }
        self.response = requests.get(self.loc_url,headers=self.headers,params=self.params)
        return self.response.json()

    def GetLocationsDetails(self,entity_id=None,entity_type=None):
        self.entity_id,self.entity_type = entity_id,entity_type
        self.LocDet = self.base_url + "location_details"
        if self.entity_id == None or self.entity_type == None:
            return "entity_id and entity_type can't be None"
        self.params = {
            'entity_id'     :"{}".format(self.entity_id),
            'entity_type' :"{}".format(self.entity_type)
        }
        self.response = requests.get(self.LocDet,headers = self.headers,params=self.params)
        return self.response.json()

    def GetDailyMenu(self,res_id=None):
        # res_id is the restaurant id of the restaurant that you're requesting the menu from.
        self.res_id = res_id
        if self.res_id is None:
            return "Error! res_id can't be None"
        self.dailyMenu = self.base_url + "dailymenu"
        self.params = {
            'res_id'  : "{}".format(self.res_id)
        }
        self.response = requests.get(self.dailyMenu,headers=self.headers,params=self.params)
        return self.response.json()

    def GetRestaurantDetails(self,res_id=None):
        # needs resturant id
        self.res_id = res_id
        if self.res_id is None:
            return "res_id cannot be None"
        self.resDet = self.base_url + "restautant"
        self.params = {
            'res_id' : "{}".format(self.res_id)
        }
        self.response = requests.get(self.resDet,headers=self.headers,params=self.params)
        return self.response.json()

    def GetRestaurantReviews(self,res_id=None):
        # needs resturant id
        self.res_id = res_id
        if self.res_id is None:
            return "res_id cannot be None"
        self.resRev = self.base_url + "reviews"
        self.params = {
            'res_id' : "{}".format(self.res_id)
        }
        self.response = requests.get(self.resRev,headers=self.headers,params=self.params)
        return self.response.json()

if __name__ == '__main__':
    app = ZomatoApi(credentials['API_KEY'])
    v = app.GetResturantCollections()
    print(v['collections'][1].values())
    print(v['collections'][1]['title'])
    print(v['collections'][1]['image_url'])
