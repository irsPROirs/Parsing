import requests

pas = 'f146ac7e032ba010'
target = 'www.google.com'
device = '2'
url = f'http://api.page2images.com/restfullink?p2i_url={target}&p2i_key={pas}&p2i_device={device}'
r = requests.get(url)
pic = r.content
with open('map.jpg', 'wb') as f:
    f.write(pic)
