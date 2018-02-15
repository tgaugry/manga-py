from src.provider import Provider
from .helpers.std import Std


class LeoMangaCom(Provider, Std):

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-')
        return '{:0>3}-{}'.format(*idx)

    def get_chapter_index(self) -> str:
        url = self.get_current_chapter()
        idx = self.re.search(r'/manga/[^/]+/capitulo-(\d+)/([^/]+)/', url).groups()
        return '{1}-{0}'.format(*idx)

    def get_main_content(self):
        name = self.get_manga_name()
        return self.http_get('{}/manga/{}'.format(self.get_domain(), name))

    def get_manga_name(self) -> str:
        return self.re.search('/manga/([^/]+)', self.get_url()).group(1)

    def _get_first_href(self, parser):
        n = self.http().normalize_uri
        url = n(parser[0].get('href'))
        select0 = self.html_fromstring(url, '.list-group .cap-option')
        if select0:
            return n(select0[0].get('href'))
        return None

    def get_chapters(self):
        n = self.http().normalize_uri
        chapter0 = self.document_fromstring(self.get_storage_content(), '.caps-list a')
        if chapter0:
            url = self._get_first_href(chapter0)
            if url:
                select0 = self.html_fromstring(url, '.viewcap-info select.form-control', 0)
                return [n(i.get('value')) for i in select0.cssselect('option')[::-1]]
        return []

    def get_files(self):
        n = self.http().normalize_uri
        items = self.html_fromstring(self.get_current_chapter(), '.vertical .cap-images')
        return [n(i.get('src')) for i in items]

    def get_cover(self) -> str:
        return self._cover_from_content('.cover img', 'data-original')


main = LeoMangaCom