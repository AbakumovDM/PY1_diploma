import requests
# import time
# from progress.bar import IncrementalBar

with open('token.txt', 'r', encoding='utf-8') as file_object:
    token = file_object.read().strip()

class VkDownloader:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access token': token,
            'v': version
        }

    def download_photos(self, owner_id, count=5):
        download_photos_url = self.url + 'photos.get'
        download_photos_params = {
            'owner_id': owner_id,
            'extended': 1,
            'album_id': 'profile',
            'photo_sizes': 1,
            'count': count
        }
        req = requests.get(download_photos_url, params={**self.params, **download_photos_params}).json()
        print(req)

    def upload(self, ya_token, owner_id):
        url = "https://cloud-api.yandex.net:443/v1/disk/resources/upload"
        headers = {'Authorization': 'OAuth {}'.format(ya_token)}
        # mylist = [1, 2, 3, 4, 5, 6, 7, 8]
        # bar = IncrementalBar('Countdown', max=len(mylist))
        # for step in mylist:
        #     bar.next()
        #     step.sleep(1)
        for item in self.download_photos(owner_id)["response"]["items"]:
            photo_name = item["likes"]["count"]
            params = {"path": f"vk_photos/{photo_name}.jpg"}
            response = requests.get(url=url, headers=headers, params=params)
            # return pprint(response.json())
            for var_photo in item["sizes"]:
                if var_photo["type"] == 'w':
                    photo_to_upload = var_photo["url"]
                resp = requests.put(response.json()['href'], data=open(photo_to_upload, 'rb'))
                if resp.status_code == 201:
                    return print("Файл успешно загружен")
            # print(resp.status_code)
        # bar.finish()
download_vk = VkDownloader(token, 5.131)
download_vk.download_photos(552934290)


