# TODO: Fully REWORK this!


from django.http import Http404


class PaginationCreator:
    def __init__(self, page: str, limit: int) -> None:
        self.page = page
        self.limit = limit

    @property
    def get_offset(self) -> int:
        try:
            page = int(self.page)
        except (TypeError, ValueError):
            page = 1

        if page > 0:
            return (page - 1) * self.limit
        else:
            raise Http404()

    @property
    def get_page(self) -> int:
        try:
            return int(self.page)
        except (TypeError, ValueError):
            return 1
