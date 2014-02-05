import calendar

def date_to_str(date):
    if type(date) in (int, long, basestring):
        return date
    elif hasattr(date, 'timetuple'):
        return calendar.timegm(date.timetuple())
    else:
        raise TypeError('Must be called with date/datetime, string, or int')
