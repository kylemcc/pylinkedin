import calendar
import urllib

def date_to_str(date):
    if type(date) in (int, long, basestring):
        return date
    elif hasattr(date, 'timetuple'):
        return calendar.timegm(date.timetuple())
    else:
        raise TypeError('Must be called with date/datetime, string, or int')

def args_to_dict(**kwargs):
    return dict([(k, v) for k, v in kwargs.iteritems() if v])

def build_url_with_qs(base_url, args):
    return '%s?%s' % (base_url, urllib.urlencode(args, True)) if args else \
            base_url