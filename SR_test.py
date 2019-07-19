import Safe_Request
import bs4
import requests

Requester = Safe_Request.Safe_Requester(5,7)
print(Requester.times)
print(Requester.count)

response = Requester.SR('https://www.geeksforgeeks.org/python-map-function/')
suuup = bs4.BeautifulSoup(response.content).prettify()

print(suuup)
