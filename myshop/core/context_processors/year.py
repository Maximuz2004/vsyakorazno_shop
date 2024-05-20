from datetime import datetime


def year(request):
    year = int(datetime.today().strftime('%Y'))
    return {
        'year': year
    }
