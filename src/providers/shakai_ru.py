from src.provider import Provider


class ShakaiRu(Provider):
    __local_storage = None

    def get_archive_name(self) -> str:
        idx = self.get_chapter_index().split('-', 2)
        return 'vol_{:0>3}-{}'.format(
            idx[0],
            1 if len(idx) < 2 else idx[1]
        )

    def get_chapter_index(self) -> str:
        idx = self.get_current_chapter().get('data-first')
        return idx.replace('_', '-')

    def get_main_content(self):
        if self.__local_storage:
            return self.__local_storage
        idx = self.re.search('/manga[^/]*/(\\d+)', self.get_url()).group(1)
        _ = {
            'dataRun': 'api-manga',
            'dataRequest': idx
        }
        page_content = str(self.http_post('http://shakai.ru/take/api-manga/request/shakai', data=_))
        return self.json.loads(page_content)

    def get_manga_name(self) -> str:
        if not self.__local_storage:
            self.__local_storage = self.get_main_content()
        parser = self.__local_storage.get('post', [])
        idx = self.re.search('/manga[^/]*/(\\d+)', self.get_url()).group(1)
        parser = parser[3] if len(parser) > 3 else idx
        return parser.split('/')[0].strip()

    def get_chapters(self):
        _ = self.get_storage_content().get('data', [])
        return _[::-1]

    def prepare_cookies(self):
        pass

    def get_files(self):
        chapter = self.get_current_chapter()
        if isinstance(chapter, dict):
            return chapter.get('data-second', [])
        return []

    def _loop_callback_chapters(self):
        pass

    def _loop_callback_files(self):
        pass


main = ShakaiRu