class FlexPageResolver:
    """
    This class contains utilities for determining the page number on which a particular object is located
    in a paginated list (either through a QuerySet or through a ForeignKey relationship).
    """

    @staticmethod
    def get_page_for_paginated_obj(
        obj,
        child_obj,
        child_paginated_objs_label: str,
        paginate_by: int,
        ordered_by: str,
    ):
        """We can flexibly get page number by existing obj, and it's paginated children(fk)"""

        if hasattr(obj, child_paginated_objs_label):
            siblings_qs = getattr(obj, child_paginated_objs_label).all().order_by(ordered_by)
            ids = list(siblings_qs.values_list('id', flat=True))

            try:
                index = ids.index(child_obj.id)
            except ValueError:
                return None

            page_number = (index // paginate_by) + 1
            return page_number

    @staticmethod
    def get_page_for_paginated_qs(qs, target_obj, paginate_by: int):
        """Here we can flexibly get page number by queryset itself and target to find its page location"""

        ids = list(qs.values_list('id', flat=True))
        try:
            index = ids.index(target_obj.id)
        except ValueError:
            return None

        page_number = (index // paginate_by) + 1
        return page_number


page_resolver = FlexPageResolver()
