from src.provider import Provider
from .helpers.std import Std
from urllib.parse import unquote_plus


class ReadHentaiMangaCom(Provider, Std):

    def get_archive_name(self) -> str:
        return 'vol_' + self.get_chapter_index()

    def get_chapter_index(self) -> str:
        return self.re.search(r'\.com/[^/]+/([^/]+)', self.chapter).group(1)

    def get_main_content(self):
        return self._get_content('{}/{}/')

    def get_manga_name(self) -> str:
        return self._get_name(r'\.com/([^/]+)')

    def get_chapters(self):
        return self._elements('ul.lst a.lst')

    def get_files(self):
        content = self.http_get(self.chapter)
        escaped_images = self.re.search(r'_img_lst\s*=.+?unescape\(\'(.+)\'\)', content)
        if escaped_images:
            return self.json.loads(unquote_plus(escaped_images.group(1)))
        return []

    def get_cover(self) -> str:
        return self._cover_from_content('img.cvr')


main = ReadHentaiMangaCom
