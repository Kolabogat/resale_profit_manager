TICKETS_FILTER_STATE = (
    {
        'pk': 1,
        'title': 'Profit Waiting',
        'query_value': 'profit=None',
        'url_value': 'profit_waiting',
        'annotation': 'Filter tickets by profit none',
        'css_style': 'bg-orange',
    },
    {
        'pk': 2,
        'title': 'Profit Failure',
        'query_value': 'profit__lt=0',
        'url_value': 'profit_failure',
        'annotation': 'Filter tickets by profit failure',
        'css_style': 'bg-red',
    },
    {
        'pk': 3,
        'title': 'Profit Nothing',
        'query_value': 'profit=0',
        'url_value': 'profit_nothing',
        'annotation': 'Filter tickets without profit',
        'css_style': 'bg-yellow',
    },
    {
        'pk': 4,
        'title': 'Profit Success',
        'query_value': 'profit__gt=0',
        'url_value': 'profit_success',
        'annotation': 'Filter tickets by profit success',
        'css_style': 'bg-green',
    },
)

TICKET_FILTERS_ORDER_BY = (
    {
        'pk': 5,
        'title': 'Ascending Title',
        'query_value': 'title',
        'url_value': 'title_asc',
        'annotation': 'Filter tickets by title.',
    },
    {
        'pk': 6,
        'title': 'Descending Title',
        'query_value': '-title',
        'url_value': 'title_desc',
        'annotation': 'Filter tickets by title.',
    },
    {
        'pk': 7,
        'title': 'Ascending Bought',
        'query_value': 'bought',
        'url_value': 'bought_asc',
        'annotation': 'Filter tickets by bought from lowest to highest',
    },
    {
        'pk': 8,
        'title': 'Descending Bought',
        'query_value': '-bought',
        'url_value': 'bought_desc',
        'annotation': 'Filter tickets by bought from highest to lowest',
    },
    {
        'pk': 9,
        'title': 'Ascending Sold',
        'query_value': 'sold',
        'url_value': 'sold_asc',
        'annotation': 'Filter tickets by sold from lowest to highest',
    },
    {
        'pk': 10,
        'title': 'Descending Sold',
        'query_value': '-sold',
        'url_value': 'sold_desc',
        'annotation': 'Filter tickets by sold from highest to lowest',
    },
    {
        'pk': 11,
        'title': 'Ascending Profit',
        'query_value': 'profit',
        'url_value': 'profit_asc',
        'annotation': 'Filter tickets by profit from lowest to highest',
    },
    {
        'pk': 12,
        'title': 'Descending Profit',
        'query_value': '-profit',
        'url_value': 'profit_desc',
        'annotation': 'Filter tickets by profit from highest to lowest',
    },
    {
        'pk': 13,
        'title': 'Ascending Date',
        'query_value': 'created_at',
        'url_value': 'date_asc',
        'annotation': 'Filter tickets by earliest date',
    },
    {
        'pk': 14,
        'title': 'Descending Date',
        'query_value': '-created_at',
        'url_value': 'date_desc',
        'annotation': 'Filter tickets by earliest date',
    },
)

# Constants for UserSettings model
CURRENCY = (
    {
        'pk': 1,
        'currency': '$',
    },
    {
        'pk': 2,
        'currency': '€',
    },
    {
        'pk': 3,
        'currency': '₽',
    },
    {
        'pk': 4,
        'currency': '₴',
    },
    {
        'pk': 5,
        'currency': 'L',
    },
)

# Constants for UserSettings model
PAGINATION = (
    {
        'pk': 1,
        'paginate_by': 5,
    },
    {
        'pk': 2,
        'paginate_by': 10,
    },
    {
        'pk': 3,
        'paginate_by': 15,
    },
    {
        'pk': 4,
        'paginate_by': 25,
    },
    {
        'pk': 5,
        'paginate_by': 50,
    },
    {
        'pk': 6,
        'paginate_by': 100,
    },
    {
        'pk': 7,
        'paginate_by': 200,
    },
)
