import requests

with open('token.txt', 'r', encoding='utf-8') as file_object:
    token = file_object.read()

with open('ya_token.txt', 'r', encoding='utf-8') as file_object:
    ya_token = file_object.read()

class VkDownloader:
    url = 'https://api.vk.com/method/'
    def __init__(self, token, version):
        self.params = {
            'access_token': token,
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
        return req

    def upload(self, ya_token, owner_id):
        url = "https://cloud-api.yandex.net:443/v1/disk/resources/upload"
        headers = {'Authorization': 'OAuth {}'.format(ya_token)}
        for item in self.download_photos(owner_id)["response"]["items"]:
            photo_name_1 = item["likes"]["count"]
            photo_name_2 = item["id"]
            photo_name = f'{photo_name_1} _ {photo_name_2}'
            params = {"path": f"vk_photos/{photo_name}.jpg", "overwrite": "true"}
            response = requests.get(url=url, headers=headers, params=params)
            for var_photo in item["sizes"]:
                if var_photo["type"] == 'y':
                    photo_to_upload = requests.get(var_photo["url"]).content
                    resp = requests.put(response.json()['href'], data=photo_to_upload)
                    if resp.status_code == 201:
                        print("Файл успешно загружен")

download_vk = VkDownloader(token, 5.131)
download_vk.download_photos(552934290)
download_vk.upload(ya_token, 552934290)

