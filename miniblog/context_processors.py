import datetime


def get_current_data_to_context(request):
    current_datetime = datetime.datetime.now()
    return {
        'current_year': current_datetime.year,
        'current_user': request.user,
    }