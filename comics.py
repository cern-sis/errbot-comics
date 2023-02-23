from errbot import BotPlugin
import requests
from bs4 import BeautifulSoup
from datetime import date
import io
from schedule import repeat, every, run_pending


class Comics(BotPlugin):
    def zulip(self):
        return self._bot.client

    def activate(self):
        super().activate()
        self.start_poller(60, self.run)

    def run(self):
        run_pending()

    @repeat(every().day.at("08:30"))
    def dilbert(self):
        today = f"{date.today():%Y-%m-%d}"
        url = f"https://dilbert.com/strip/{today}"
        page = requests.get(url)
        html = BeautifulSoup(page.text, "html.parser")
        html_img = html.find("img", class_="img-comic")

        img = requests.get(html_img["src"])

        with io.BytesIO(img.content) as i:
            i.name = f"dilbert-{today}.gif"
            result = self.zulip().upload_file(i)

        self.send(
            self.build_identifier("#{{off-topic}}*{{Dilbert}}"),
            f"[{html_img['alt']}]({result['uri']})\n\n[Source]({url})",
        )
