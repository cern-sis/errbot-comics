from errbot import BotPlugin, botcmd
import requests
from bs4 import BeautifulSoup
from datetime import date
import io


class Comics(BotPlugin):
    def zulip(self):
        return self._bot.client

    @botcmd
    def dilbert(self, msg, args):
        today = f"{date.today():%Y-%m-%d}"
        url = f"https://dilbert.com/strip/{today}"
        page = requests.get(url)
        html = BeautifulSoup(page.text, "html.parser")
        html_img = html.find("img", class_="img-comic")

        img = requests.get(html_img["src"])

        with io.BytesIO(img.content) as i:
            i.name = f"dilbert-{today}.gif"
            result = self.zulip().upload_file(i)

            return f"[{html_img['alt']}]({result['uri']})\n\n[Source]({url})"
