import requests


class Insta:
    account = {}
    reels_ids = []
    username = ""
    private = False
    posts_data = {}

    header = {
        "user-agent": 'Mozilla/5.0 (Linux; Android 8.1.0; motorola one Build/OPKS28.63-18-3; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 '
                      'Chrome/70.0.3538.80 Mobile Safari/537.36 Instagram 72.0.0.21.98 Android (27/8.1.0; 320dpi; 720x1362; motorola; motorola one; '
                      'deen_sprout; qcom; pt_BR; 132081645) ',
    }

    cookies = {
        'sessionid': ''
    }

    def __init__(self, username: str):
        self.load(username)
        self.thumbnails(show=False)
        self.username = username
        if self.account['data']['user']['is_private']:
            print("Le compte est privÃ©")
            self.private = True
        else:
            r = requests.get(
                f"https://i.instagram.com/api/v1/feed/user/{self.username}/username/?count={self.account['data']['user']['edge_owner_to_timeline_media']['count']}",
                headers=self.header)
            self.posts_data = r.json()

    def load(self, username: str) -> None:
        r = requests.get("https://www.instagram.com/api/v1/users/web_profile_info/?username=" + username, headers=self.header, cookies=self.cookies)
        self.account = r.json()

    def thumbnails(self, show=True) -> None:
        if not self.private:
            r = requests.get("https://www.instagram.com/graphql/query/?query_hash=d4d88dc1500312af6f937f7b804c68c3&variables=%7B%22user_id%22%3A%22"
                             + self.account['data']['user']['id'] + "%22%2C%22include_chaining%22%3Atrue%2C%22include_reel%22%3Afalse%2C%22include_suggested_users" +
                             "%22%3Afalse%2C%22include_logged_out_extras%22%3Afalse%2C%22include_highlight_reels%22%3Atrue%2C%22include_live_status%22%3Atrue%7D",
                             cookies=self.cookies, headers=self.header)
            if show:
                print("Thumbnails :")
            for real in r.json()['data']['user']['edge_highlight_reels']['edges']:
                if show:
                    print(real['node']['cover_media']['thumbnail_src'])
                else:
                    self.reels_ids.append('highlight:' + real['node']['id'])

    def reels(self, wich=0) -> None:
        if not self.private:
            params = {
                'reel_ids': self.reels_ids,
            }
            r = requests.get('https://www.instagram.com/api/v1/feed/reels_media/', params=params, cookies=self.cookies, headers=self.header)
            i = 0
            print("Reels :")
            for reals in r.json()['reels']:
                if wich == 0 or i == wich - 1:
                    print(r.json()['reels'][reals]['title'])
                    for pic in r.json()['reels'][reals]['items']:
                        print(pic['image_versions2']['candidates'][0]['url'])
                i += 1

    def pp(self):
        print("Profile picture :")
        print(self.account['data']['user']['profile_pic_url_hd'])

    def posts(self):
        if not self.private:
            print("Posts :")
            for item in self.posts_data['items']:
                if 'image_versions2' in item:
                    link = item['image_versions2']['candidates'][0]['url']
                    print(link)
                    # if open_all == "y":
                    #     webbrowser.open(link)
                elif 'carousel_media' in item:
                    for media in item['carousel_media']:
                        link = media['image_versions2']['candidates'][0]['url']
                        print(link)
                        # if open_all == "y":
                        #     webbrowser.open(link)

    def post(self, num=None):
        if not self.private:
            if num is not None:
                print("Post :")
                for pic in self.posts_data['items']:
                    if pic['code'] == num:
                        if 'image_versions2' in pic:
                            link = pic['image_versions2']['candidates'][0]['url']
                            print(link)
                            # if open_all == "y":
                            #     webbrowser.open(link)
                        elif 'carousel_media' in pic:
                            for media in pic['carousel_media']:
                                link = media['image_versions2']['candidates'][0]['url']
                                print(link)
                                # if open_all == "y":
                                #     webbrowser.open(link)
            else:
                print("Veuillez renseigner le code de la publication")

    def story(self):
        if not self.private:
            r = requests.get("https://www.instagram.com/api/v1/feed/reels_media/?reel_ids="+self.account['data']['user']['id'], cookies=self.cookies, headers=self.header)
            print("Story :")
            for i in r.json()['reels']:
                item = r.json()['reels'][i]
                for pic in item['items']:
                    print(pic['image_versions2']['candidates'][0]['url'])
