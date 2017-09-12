from yelpapi import YelpAPI
from credentials import yelp_creds


client_id = yelp_creds['client_id']
client_secret = yelp_creds['client_secret']

def yelp_search(coords = (-122.4392,37.7474)):
    yelp_api = YelpAPI(client_id, client_secret)
    search_results = yelp_api.search_query(categories='tacos', longitude=coords[0], latitude=coords[1], limit=10)
    return search_results

def get_res_info(search_results):
    res_list = []
    for x in range(len(search_results['businesses'])):
        res_name = search_results['businesses'][x]['name']
        res_rating = search_results['businesses'][x]['rating']
        res_review_count = search_results['businesses'][x]['review_count']
        res_currency = search_results['businesses'][x]['price']
        res_currency = search_results['businesses'][x]['image_url']
        res_addr = search_results['businesses'][x]['location']['address1']
        res_list.append((res_name,res_rating,res_review_count,res_currency,res_addr))
    return res_list

x = yelp_search()
print(get_res_info(x))
