
# zomato wrap : Zomato wrap is an api wrapper.

import requests

credentials = {
                # zomato api key to access taco resturant data
                "API_KEY":""
}

class ZomatoApi():

    def __init__(self,API_KEY):
        self.API_KEY = API_KEY
        self.base_url = "https://developers.zomato.com/api/v2.1/"
        # the api key is passed in the header of the url
        self.headers = {"user-key":"{}".format(self.API_KEY)}

    def search(self,lat,lon,limit,count):
        self.lat = lat
        self.lon = lon
        self.limit = limit
        self.count = count 
        self.search_url = self.base_url + "search"

        self.params = {
            'lat' : "{}".format(self.lat),
            'lon' : "{}".format(self.lon),
            'count':"{}".format(self.count),
            'limit':"{}".format(self.limit),
            'cuisines':"{}".format(997)
        }

        self.response = requests.get(self.search_url,headers=self.headers,params=self.params)
        return self.response.json()

    def packDetails(self,jsonObj):
        final_list = []
        for n in range(0,len(jsonObj['restaurants'])-1):
            rName = jsonObj["restaurants"][n]['restaurant']['name']
            rImg = jsonObj["restaurants"][n]['restaurant']['featured_image']
            rRate = jsonObj["restaurants"][n]['restaurant']['user_rating']['aggregate_rating']
            rLoc = jsonObj["restaurants"][n]['restaurant']['location']['address']
            rPrice = jsonObj["restaurants"][n]['restaurant']['price_range']
            if rImg is '':
                # load default image
                rImg = "http://weknowyourdreams.com/images/food/food-08.jpg"
            final_list.append((rName,rImg,rRate,rLoc,rPrice))
        return final_list

# taco - 997
# new mexican - 995
# mexican - 73

if __name__ == '__main__':
    app = ZomatoApi(credentials['API_KEY'])
    v = app.search(40.730610,-73.935242,2,5)
    #print(v.keys())
    x = app.packDetails(v)
    for y in x:
        print(y)
    #app.CompareAndRate(x)
