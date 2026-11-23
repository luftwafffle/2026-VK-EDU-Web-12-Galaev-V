from django.core.paginator import Paginator



def paginate(objects_list, request, per_page=20):    # не вьюха
    paginator = Paginator(objects_list, per_page)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    page_obj.elided_range = paginator.get_elided_page_range(page_obj.number, on_each_side=2, on_ends=1)
    return page_obj