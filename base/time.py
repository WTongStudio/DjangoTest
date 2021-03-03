# -*- coding: utf-8 -*-
# 时间处理相关方法

import pytz
from datetime import datetime, timedelta, date, time as _time
import calendar
import time
import datetime as _datetime

from django.utils import timezone

bjtz = pytz.timezone('Asia/Shanghai')
utc = pytz.timezone('UTC')

ONE_MINUTE = 60
TWO_MINUTE = 60 * 2
ONE_HOUR = 60 * 60
ONE_DAY = 24 * 60 * 60

LIVEME_AREA_TIMEZONE = {
    'A_US': 'Etc/GMT+7',
    'A_US_WINTER': 'Etc/GMT+8',
    'A_CT': 'Etc/GMT-8',
    'A_JP': 'Etc/GMT-9',
    'A_ID': 'Etc/GMT-8',  # 印度尼西亚分区
    'A_AR': 'Etc/GMT-3',  # 阿拉伯分区
    'A_DE': 'Etc/GMT-1',  # 德国分区
    'A_IN': 'Etc/GMT-5',  # 印度分区
    'A_VN': 'Etc/GMT-7',  # 越南分区
    'A_BR': 'Etc/GMT+3',  # 巴西分区
    # 'A_GB': 'Etc/GMT+0', #英国分区
}

TIMEZONE_OFFSET = {
    'A_US': -7,
    'A_CT': 8,
    'A_JP': 9,
    'A_ID': 8,  # 印度尼西亚分区
    'A_AR': 3,  # 阿拉伯分区
    'A_DE': 1,  # 德国分区
    'A_IN': 5.5,  # 印度分区
    'A_VN': 7,  # 越南分区
    'A_BR': -3,  # 巴西分区
    # 'A_GB': 0, #英国分区
    'A_US_WINTER': -8,
}

TIMEZONE_WEB_OFFSET = {
    'A_US_0': -7,  # 美国夏令时
    'A_US_1': -8,  # 美国冬令时
    'A_CHN': 8,  # 北京时间
    'A_GT': 1,
    'A_AR': 3,  # 中东区
    'A_BR_0': -2,  # 巴西分区 夏令时
    'A_BR_1': -3,  # 巴西分区 冬令时
    'A_CT': 8,  # 台湾区
    'A_ID': 8,  # 印度尼西亚分区
    'A_IN': 5.5,  # 印度区
    'A_JP': 9,  # 日本区
}

MONTH_DAY = {
    '1': 31,
    '2': 28,
    '3': 31,
    '4': 30,
    '5': 31,
    '6': 30,
    '7': 31,
    '8': 31,
    '9': 30,
    '10': 31,
    '11': 30,
    '12': 31,
}


# http://stackoverflow.com/questions/24856643/unexpected-results-converting-timezones-in-python
def str_bjtime(dt, fmt='%Y-%m-%d %H:%M:%S', with_timezone=False):
    """将数据库取出来的时间转化为北京时间字符串"""
    if not dt or not isinstance(dt, (datetime, date, _time)):
        # 取出来的值为空或者不是日期类型，直接返回
        return dt
    if not dt.tzinfo:
        # 没有时间戳信息，加上utc
        dt = pytz.utc.localize(dt)
    bjdt = dt.astimezone(bjtz)

    if with_timezone:
        fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    str_time = bjdt.strftime(fmt)
    return str_time


def bjstr_to_time(dt_str):
    """将时间字符串转化为带有时间戳的datetime类型"""
    formats = ['%Y-%m-%d %H:%M', '%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y%m%d']
    for format in formats:
        try:
            dt = datetime.strptime(dt_str, format)
            # 默认认为时间字符串所表示的是北京时间
            bjdt = bjtz.localize(dt)
            utcdt = bjdt.astimezone(pytz.utc)
            return utcdt
        except:
            pass
    return


def translate_timezone(date_time, tz=None, area=None):
    """
    时区转换
    1. 如果tz有值，直接根据提供的timezone进行时区转换
    2. 如果area有值，根据大区所在的时区进行时区转换
    :param date_time:
    :param tz:
    :param area:
    :return:
    """
    if not isinstance(date_time, datetime):
        raise TypeError('Param `date_time` type must be datetime.datetime')

    if not date_time.tzinfo:
        raise ValueError('Param `date_time` timezone is empty')

    if not (tz or area):
        raise ValueError('Params [`timezone`, `area`] can not empty')

    if tz:
        return date_time.astimezone(tz)

    if area:
        _tz = LIVEME_AREA_TIMEZONE.get(area, 'Etc/GMT+7')
        _tz = pytz.timezone(_tz)
        return date_time.astimezone(_tz)


def utc_string_to_datetime(utc_string, timezone_offset=0):
    """
    将时间字符串转化为带有时间戳的datetime类型
    :param utc_string: 时间字符串
    :param timezone_offset: 相对UTC的偏移量 单位：小时
    """
    formats = ['%Y-%m-%d %H:%M', '%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y%m%d']
    for _format in formats:
        try:
            dt = datetime.strptime(utc_string, _format)
        except:
            continue
        utc_dt = utc.localize(dt)
        return utc_dt - timedelta(hours=timezone_offset)
    return


def date2timestamp(dt):
    # datetime to timestamp
    import calendar
    if not isinstance(dt, datetime):
        return datetime
    if not dt.tzinfo:
        # 没有时间戳信息，加上utc
        dt = pytz.utc.localize(dt)
    dt = dt.astimezone(utc)
    timestamp = calendar.timegm(dt.utctimetuple()) + dt.microsecond / 1e6
    return timestamp


def timestamp2date(timestamp):
    try:
        timestamp = int(timestamp)
    except:
        return timestamp
    if not isinstance(timestamp, (int, float)):
        return timestamp
    date = datetime.utcfromtimestamp(timestamp)
    utcdt = pytz.utc.localize(date)
    return utcdt


def now(tz='utc'):
    """返回带有时间戳的当前时间，默认为utc时间"""
    if tz == 'beijing':
        return datetime.now(bjtz)
    return datetime.now(pytz.utc)


# now的实际意义
now_with_tz = now


def today_begin_with_tz():
    """获取北京当前时间的开始时间"""
    today_begin = datetime.combine(now(tz='beijing').date(), datetime.min.time())
    return bjtz.localize(today_begin)


def start_end_this_week():
    """返回当前所在周的开始时间和结束时间"""
    tb = today_begin_with_tz()
    start = tb - timedelta(days=tb.weekday())
    end = start + timedelta(days=7)
    return start, end


def weekday_to_zh(weekday):
    if not isinstance(weekday, int) or weekday < 0 or weekday > 6:
        return weekday
    days_zh = [u'周一', u'周二', u'周三', u'周四', u'周五', u'周六', u'周日']
    return days_zh[weekday]


def format_time(dt, format='%m月%d日 %H:%M'):
    '''datetime格式化成字符串'''
    if not (dt and isinstance(dt, datetime)):
        return ''
    if not dt.tzinfo:
        # 没有时间戳信息，默认为utc
        dt = pytz.utc.localize(dt)
    dt = dt.astimezone(bjtz)
    return unicode(dt.strftime(format), 'utf-8')


def format_utc_str_to_datetime(utc_str):
    """2017-01-05T10:49:13.135202+00:00"""
    import dateutil.parser
    if not (utc_str and isinstance(utc_str, (str, unicode))):
        return datetime
    return dateutil.parser.parse(utc_str)


def get_week_of_month(dt_day):
    """
    获取当前日期在本月中是第几周的周几
    :param dt_day: datetime day
    :return: int, int   # 第几周，周几（周一至周日用0~6表示）
    """
    if not isinstance(dt_day, datetime):
        return 0, 0

    day_week = int(dt_day.strftime('%W'))
    _dt_day = dt_day
    _mont_first_day = _dt_day.replace(day=1)
    first_day_week = int(_mont_first_day.strftime('%W'))
    return day_week - first_day_week + 1, dt_day.weekday()


def get_us_dst_range(year):
    """
    获取美国夏令时时间范围
    美国夏令时一般在3月第二个周日凌晨2AM（当地时间）开始，将时钟调到3点，拨快1小时，俗称“Spring Forward 1 Hour”；
    而在11月第一个周日凌晨2AM（当地时间）夏令时结束，要将时钟调到1点，拨慢1小时，俗称“Fall Back 1 Hour”。
    :param year:
    :return: datetime start with us timezone, datetime end with us timezone
    """
    utc_now = timezone.now()
    us_now = translate_timezone(utc_now, area='A_US')
    us_start = us_now.replace(year=year, month=3, day=1, hour=3, minute=0, second=0, microsecond=0)
    us_end = us_now.replace(year=year, month=11, day=1, hour=2, minute=0, second=0, microsecond=0)

    offset_day_3 = 7
    week_of_month, weekday = get_week_of_month(us_start)
    if weekday != 6:
        offset_day_3 += 6 - weekday
    us_start += timedelta(days=offset_day_3)

    offset_day_11 = 0
    week_of_month, weekday = get_week_of_month(us_end)
    if weekday != 6:
        offset_day_11 += 6 - weekday
    us_end += timedelta(days=offset_day_11)

    return us_start, us_end


def get_us_dst_winter_range(year_range):
    """
    根据年份范围获取美区冬令时夏令时时间范围
    :param year_range: 年份范围 如：[2020, 2021]
    :return: 冬令时夏令时日期范围，如: [(-8, datetime.datetime(2020, 1, 1, 0, 0), datetime.datetime(2020, 3, 8, 2, 0)),
                                    (-7, datetime.datetime(2020, 3, 8, 3, 0), datetime.datetime(2020, 11, 1, 2, 0)),
                                    (-8, datetime.datetime(2020, 11, 1, 1, 0), datetime.datetime(2021, 3, 14, 2, 0)),
                                    (-7, datetime.datetime(2021, 3, 14, 3, 0), datetime.datetime(2021, 11, 7, 2, 0)),
                                    (-8, datetime.datetime(2021, 11, 7, 2, 0), datetime.datetime(2022, 1, 1, 0, 0))]
    """
    dst_offset = TIMEZONE_OFFSET['A_US']
    win_offset = TIMEZONE_OFFSET['A_US_WINTER']
    winter_gmt = LIVEME_AREA_TIMEZONE['A_US_WINTER']
    winter_tz = pytz.timezone(winter_gmt)

    dst_winter_range = []
    perfect_dst_winter_range = []
    for year in year_range:
        dst_start, dst_end = get_us_dst_range(year)
        win_fh_start = dst_start.replace(month=1, day=1, hour=0, tzinfo=winter_tz)
        win_fh_end = dst_start + timedelta(hours=-1)
        win_lh_start = dst_end + timedelta(hours=-1)
        win_lh_end = dst_end.replace(month=12, day=31, hour=0, tzinfo=winter_tz)
        win_lh_end += timedelta(hours=24)
        win_fh_end = win_fh_end.replace(tzinfo=winter_tz)
        win_lh_start = win_lh_start.replace(tzinfo=winter_tz)
        dst_winter_range.append((win_offset, win_fh_start, win_fh_end))
        dst_winter_range.append((dst_offset, dst_start, dst_end))
        dst_winter_range.append((win_offset, win_lh_start, win_lh_end))

    for range_data in dst_winter_range:
        hour_offset = range_data[0]
        if perfect_dst_winter_range:
            last_range = perfect_dst_winter_range[-1]
            if last_range[0] == hour_offset:
                last_range = list(last_range)
                last_range[-1] = range_data[-1]
                perfect_dst_winter_range[-1] = tuple(last_range)
                continue
        perfect_dst_winter_range.append(range_data)
    return perfect_dst_winter_range


def is_winter_time(timestamp=None):
    """
    判断时间是否为美国冬令时时间
    美国夏令时一般在3月第二个周日凌晨2AM（当地时间）开始，将时钟调到3点，拨快1小时，俗称“Spring Forward 1 Hour”；
    而在11月第一个周日凌晨2AM（当地时间）夏令时结束，要将时钟调到1点，拨慢1小时，俗称“Fall Back 1 Hour”。
    (供公会后台使用)
    :param timestamp: 时间戳
    :return: boolean
    """
    if not timestamp:
        timestamp = int(time.time())

    dt_now = datetime.fromtimestamp(timestamp, tz=pytz.utc)
    us_now = translate_timezone(dt_now, area='A_US')
    dst_start, dst_end = get_us_dst_range(us_now.year)
    if dst_start <= us_now <= dst_end:
        return False
    else:
        return True


def format_timestamp_to_str_by_area(timestamp, area, ft='%Y-%m-%d %H:%M:%S'):
    """
    :param timestamp: 10位时间戳
    :param area: 大区码
    :param ft: format
    :return:
    """
    timezone = LIVEME_AREA_TIMEZONE.get(area, 'Etc/GMT-8')
    tz = pytz.timezone(timezone)
    if area == 'A_IN':
        timestamp = timestamp + 60 * 30  # 印度去是东5.5区  pytz里是东5区 所以加30分钟
    datetime_obj = datetime.fromtimestamp(timestamp, tz)
    return datetime_obj.strftime(ft)


def get_area_start_time(timestamp, area):
    """
    获取某个大区当天00:00:00时的时间戳
    :param area: 大区
    :param timestamp: 时间戳
    :return: 时间戳
    """
    timezone = LIVEME_AREA_TIMEZONE.get(area, 'Etc/GMT-8')  # 该大区的时区
    tz = pytz.timezone(timezone)
    if area == 'A_IN':
        timestamp = timestamp + 60 * 30  # 印度去是东5.5区  pytz里是东5区 所以加30分钟
    area_now_time = datetime.fromtimestamp(timestamp, tz)  # 该大区时区的此刻的时间
    dt = datetime(area_now_time.year, area_now_time.month, area_now_time.day, 0, 0, 0)
    t = tz.localize(dt)
    t = t.astimezone(pytz.utc)
    return int(time.mktime(t.utctimetuple())) - time.timezone


def get_area_end_time(timestamp, area):
    """
    获取某个大区当天23:59:59时的时间戳
    :param area: 大区
    :param timestamp: 时间戳
    :return: 时间戳
    """
    timezone = LIVEME_AREA_TIMEZONE.get(area, 'Etc/GMT-8')  # 该大区的时区
    tz = pytz.timezone(timezone)
    if area == 'A_IN':
        timestamp = timestamp + 60 * 30  # 印度去是东5.5区  pytz里是东5区 所以加30分钟
    area_now_time = datetime.fromtimestamp(timestamp, tz)  # 该大区时区的此刻的时间
    dt = datetime(area_now_time.year, area_now_time.month, area_now_time.day, 23, 59, 59)
    t = tz.localize(dt)
    t = t.astimezone(pytz.utc)
    return int(time.mktime(t.utctimetuple())) - time.timezone


def is_run_year(year):
    if year % 4 == 0 and year % 100 == 0 and year % 400 == 0:
        return True
    return False


def get_area_month_end_time(timestamp, area):
    """
    获取某个大区月末23:59:59时的时间戳
    :param area: 大区
    :param timestamp: 时间戳
    :return: 时间戳
    """
    area_end_time = get_area_end_time(timestamp, area)
    timezone = LIVEME_AREA_TIMEZONE.get(area, 'Etc/GMT-8')  # 该大区的时区
    tz = pytz.timezone(timezone)
    if area == 'A_IN':
        area_now_time = datetime.fromtimestamp(timestamp + 60 * 30, tz)  # 印度去是东5.5区  pytz里是东5区 所以加30分钟
    else:
        area_now_time = datetime.fromtimestamp(timestamp, tz)  # 该大区时区的此刻的时间
    month = area_now_time.month
    day = area_now_time.day
    end_day = MONTH_DAY[str(month - 1)]
    if month == 2:
        year = area_now_time.year
        # 判断是否为闰年
        if is_run_year(year):
            end_day = end_day + 1
    return area_end_time + (end_day - day) * 24 * 60 * 60


def get_area_month_start_time(timestamp, area):
    """
    获取某个大区月初00:00:00时的时间戳
    :param area: 大区
    :param timestamp: 时间戳
    :return: 时间戳
    """
    area_start_time = get_area_start_time(timestamp, area)
    timezone = LIVEME_AREA_TIMEZONE.get(area, 'Etc/GMT-8')  # 该大区的时区
    tz = pytz.timezone(timezone)
    if area == 'A_IN':
        area_now_time = datetime.fromtimestamp(timestamp + 60 * 30, tz)  # 印度去是东5.5区  pytz里是东5区 所以加30分钟
    else:
        area_now_time = datetime.fromtimestamp(timestamp, tz)  # 该大区时区的此刻的时间
    day = area_now_time.day
    return area_start_time - (day - 1) * 24 * 60 * 60


def bj_date_str_and_monday_date_str(timestamp=None, format='%Y%m%d'):
    '''通过时间戳获取北京时间该天和该周一字符串'''
    if timestamp:
        dt = timestamp2date(timestamp)
    else:
        dt = now()
    date_str = str_bjtime(dt, format)
    if not dt.tzinfo:
        # 没有时间戳信息，加上utc
        dt = pytz.utc.localize(dt)
    bjdt = dt.astimezone(bjtz)
    start = bjdt - timedelta(days=bjdt.weekday())
    monday_date_str = str_bjtime(start, format)
    return date_str, monday_date_str


def start_end_this_mounth(dt):
    """返回当前所在周的开始时间和结束时间"""
    tb = today_begin_with_tz()
    start = tb - timedelta(days=tb.weekday())
    end = start + timedelta(days=7)
    return start, end


def str_bjtime_by_ts(timestamp, fmt='%Y-%m-%d %H:%M:%S'):
    '''通过时间戳获取北京时间字符串'''
    return str_bjtime(timestamp2date(timestamp), fmt)


def start_and_end_by_bjstr(dt_str):
    bjtime = bjstr_to_time(dt_str)
    start_time = bjstr_to_time(str_bjtime(bjtime, "%Y-%m-%d"))
    end_time = start_time + timedelta(days=1)
    return start_time, end_time


def bjstr_to_ts(bj_str):
    """
    :param bj_str: '20180801'
    :return: 1533052800
    """
    utc_dt = bjstr_to_time(bj_str)
    return calendar.timegm(utc_dt.utctimetuple())


def get_date_str_before_or_after_now(days):
    '''
    获取北京时间昨天时间年月日
    :return:
    '''
    today = today_begin_with_tz()
    diff = timedelta(days=days)
    want_date = today + diff
    return want_date.strftime('%Y-%m-%d')


def get_ts_by_local_date(dt, area):
    """
    :param dt: datetime
    :param area: 大区
    :return: 时间戳
    """
    if not isinstance(dt, datetime):
        return None

    if not dt.tzinfo:
        dt = pytz.utc.localize(dt)
    timezone = LIVEME_AREA_TIMEZONE.get(area, 'Etc/GMT-8')  # 该大区的时区
    tz = pytz.timezone(timezone)
    dt_with_tz = dt.astimezone(tz)

    utc_hour_offset = TIMEZONE_OFFSET.get(area, 8)
    if area == 'A_IN':
        dt_with_tz = dt_with_tz - timedelta(hours=5, minutes=30)
    else:
        dt_with_tz = dt_with_tz - timedelta(hours=utc_hour_offset)
    import calendar
    timestamp = calendar.timegm(dt_with_tz.utctimetuple()) + dt_with_tz.microsecond / 1e6
    return int(timestamp)


def get_current_datetime_by_area(area, format='%Y-%m-%d %H:%M:%S'):
    hour_offset = TIMEZONE_OFFSET.get(area, 8)
    utc_dt = datetime.utcnow()
    if area == 'A_IN':
        utc_dt = utc_dt + timedelta(hours=5, minutes=30)
    else:
        utc_dt = utc_dt + timedelta(hours=hour_offset)
    return utc_dt


def get_current_datetime_with_timezone_by_area(area):
    """
    获取当前大区的当前时间（用当前大区所在的时区表示当前时间）
    :param area: 大区
    :return: datetime.datetime object
    """
    if area == 'A_US' and is_winter_time():
        area = 'A_US_WINTER'
    area_tz = LIVEME_AREA_TIMEZONE.get(area, 'Etc/GMT+7')
    area_tz = pytz.timezone(area_tz)
    utc_now = timezone.now()
    return utc_now.astimezone(area_tz)


def timestamp_now():
    import time
    return int(time.time())


def get_area_datetime(timestamp, area):
    """
    获取时间戳在指定大区的时间
    :param area: 大区
    :param timestamp: 时间戳
    :return: datetime object
    """
    if area == 'A_US':
        if is_winter_time(timestamp):
            area = 'A_US_WINTER'
    timezone = LIVEME_AREA_TIMEZONE.get(area, 'Etc/GMT-8')  # 该大区的时区
    _tz = pytz.timezone(timezone)
    if area == 'A_IN':
        timestamp = timestamp + 60 * 30  # 印度去是东5.5区  pytz里是东5区 所以加30分钟
    area_now_time = datetime.fromtimestamp(timestamp, _tz)  # 该大区时区的此刻的时间
    return area_now_time


def get_area_time_str(timestamp, area):
    """
    获取大区时间字符串
    :param area: 大区
    :param timestamp: 时间戳
    :return: 时间字符串 20191003
    """
    if not timestamp or not area:
        return ''
    area_now_time = get_area_datetime(timestamp, area)
    return "%04d%02d%02d" % (area_now_time.year, area_now_time.month, area_now_time.day)


def get_area_datetime_str(timestamp, area):
    """
    获取大区时间字符串
    :param area: 大区
    :param timestamp: 时间戳
    :return: 时间字符串 2019-10-3 10:00:00
    """
    if not timestamp or not area:
        return ''
    area_now_time = get_area_datetime(timestamp, area)
    return area_now_time.strftime('%Y-%m-%d %H:%M:%S')


def get_current_day():
    """
    获取当前日期
    :return: %Y-%m-%d %H:%M:%S
    """
    time_now = datetime.now()
    current_day = time_now.replace(hour=23, minute=59, second=59)
    return current_day


def get_current_month_first_day():
    """
    获取当月第一天
    :return: %Y-%m-%d %H:%M:%S
    """
    time_now = datetime.now()
    month_day = time_now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return month_day


def get_day_before_current_day(days=30):
    """
    获取当前日期的第前X天
    :param days: 前多少天
    :return: %Y-%m-%d %H:%M:%S
    """
    time_now = datetime.now()
    time_before = time_now - _datetime.timedelta(days=days)
    perfect_day = time_before.replace(hour=0, minute=0, second=0, microsecond=0)
    return perfect_day


def make_perfect_rpc_params_with_timezone(area='A_US', time_zone=None, **params):
    """
    组装调用大数据接口时的参数，添加"area"和"timezone"字段
    :param area: 大区
    :param time_zone: 时区
    :param params:
    :return:
    """
    perfect_area = area
    if is_winter_time() and area == 'A_US':
        perfect_area = 'A_US_WINTER'

    if time_zone:
        time_offset = TIMEZONE_WEB_OFFSET.get(time_zone, -7)
    else:
        time_offset = TIMEZONE_OFFSET.get(perfect_area)
    params['area'] = str(area)
    params['timezone'] = time_offset
    return params


def format_datetime(dt, ft='%Y-%m-%d %H:%M:%S'):
    return dt.strftime(ft)


def month_ring_ratio_day(month_offset=0, day_time=None, use_day_end=True):
    """
    同当月或指定月份偏移指定月份
    例如：当前日期为：2020-05-06 12:00:00, 则上月为：2020-04-06 23:59:59 （day_time=None, use_day_end=True）
         指定日期为：2020-08-06 12:00:00, 则上月为：2020-07-06 23:59:59 （day_time=datetime.datetime(2020-08-06 12:00:00), use_day_end=True）
         当前日期为：2020-05-06 12:00:00, 则上月为：2020-04-06 12:00:00 （day_time=None, use_day_end=False）
         指定日期为：2020-08-06 12:00:00, 则上月为：2020-07-06 12:00:00 （day_time=datetime.datetime(2020-08-06 12:00:00), use_day_end=False）
    :param month_offset: 月份偏移量，例如：0 表示当月，-1 表示上月， +1 表示下月, 以此类推
    :param day_time: 要环比的日期
    :param use_day_end: 是否展示为日结束日期
    :return: datetime obj
    """
    if not day_time:
        day_time = timezone.now()
    if use_day_end:
        day_time = day_time.replace(hour=23, minute=59, second=59, microsecond=999999)
    first_day = day_time.replace(day=1)

    if not month_offset:
        return day_time

    def offset_month(_year, _month, offset):
        """
        偏移月份
        :param _year: 当前year
        :param _month: 当前month
        :param offset: 偏移量 （正数或负数）
        :return: year, month
        """
        _abs_offset = abs(offset)
        if offset > 0:
            _month += _abs_offset
            if _month > 12:
                while _month > 12:
                    _year += 1
                    _month -= 12
        else:
            _month -= _abs_offset
            if _month < 1:
                while _month < 1:
                    _year -= 1
                    _month += 12
        return _year, _month

    active = 1 if month_offset > 0 else -1
    abs_offset = abs(month_offset)
    month_days = 0

    if month_offset > 0:
        for index in range(abs_offset):
            year, month = offset_month(day_time.year, day_time.month, index)
            month_days += calendar.monthrange(year, month)[1]
    else:
        for index in range(1, abs_offset + 1):
            year, month = offset_month(day_time.year, day_time.month, -index)
            month_days += calendar.monthrange(year, month)[1]

    new_month_date = first_day + timedelta(days=month_days) * active
    try:
        new_month_date = new_month_date.replace(day=day_time.day)
    except ValueError:
        month_days = calendar.monthrange(new_month_date.year, new_month_date.month)[1]
        new_month_date = new_month_date.replace(day=month_days)

    return new_month_date


def base_offset_month_first_day(date_time, month_offset, time_begin=False):
    """
    偏移月份
    :param date_time:
    :param month_offset:
    :param time_begin:
    :return:
    """
    first_day = date_time.replace(day=1)
    if time_begin:
        first_day = first_day.replace(hour=0, minute=0, second=0, microsecond=0)

    while month_offset != 0:
        if month_offset < 0:
            month_offset += 1
            first_day = (first_day - timedelta(days=1)).replace(day=1)

        if month_offset > 0:
            month_offset -= 1
            first_day = (first_day.replace(day=28) + timedelta(days=4)).replace(day=1)
    return first_day


def base_offset_month(day_time=None, month_offset=0):
    """
    指定日期偏移月份
    :param day_time: datetime.datetime object
    :param month_offset: int
    :return: datetime.datetime object
    """
    if not day_time:
        day_time = timezone.now()

    if month_offset == 0:
        return day_time

    number = 1
    if month_offset < 0:
        month_offset = abs(month_offset)
        number = -1

    month_index = 0
    new_day = day_time
    while month_index != month_offset:
        month = new_day.month
        new_day += timedelta(days=1 * number)
        if new_day.month != month:
            month_index += 1

    month = new_day.month
    while True:
        if new_day.day == day_time.day:
            break
        if number < 0 and new_day.day < day_time.day:
            break
        item_day = new_day + timedelta(days=1 * number)
        if item_day.month != month:
            break
        new_day = item_day
    return new_day


def month_first_day(month_offset=0):
    """
    get month's first day
    :param month_offset:
        月份偏移量，例如：0 表示当月，-1 表示上月， +1 表示下月, 以此类推
    :return: datetime obj
    """
    today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    first_day = today.replace(day=1)
    first_day = base_offset_month_first_day(first_day, month_offset)
    return first_day


def month_first_day_end(month_offset=0):
    """
    get month's first day
    :param month_offset:
        月份偏移量，例如：0 表示当月，-1 表示上月， +1 表示下月, 以此类推
    :return: datetime obj
    """
    today = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    first_day = today.replace(day=1)
    first_day = base_offset_month_first_day(first_day, month_offset)
    return first_day


def day_begin(offset=0, date_time=None):
    """
    获取日期开始的 datetime 对象
    :param offset:
        日期偏移量，例如：0 表示当天，-1 表示上一天， +1 表示下一天, 以此类推
    :param date_time: 日期, datetime类型
    :return:
    """
    if date_time and not isinstance(date_time, datetime):
        raise TypeError('Param `current_date` type error.')

    if date_time:
        dt = date_time.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        dt = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return dt + timedelta(days=offset)


def day_end(offset=0, date_time=None):
    """
    获取日期开始的 datetime 对象
    :param offset:
        日期偏移量，例如：0 表示当天，-1 表示上一天， +1 表示下一天, 以此类推
    :param date_time: 日期, datetime类型
    :return:
    """
    if date_time and not isinstance(date_time, datetime):
        raise TypeError('Param `current_date` type error.')

    if date_time:
        dt = date_time.replace(hour=23, minute=59, second=59, microsecond=999999)
    else:
        dt = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
    return dt + timedelta(days=offset)


def get_perfect_timezone_offset(area='A_US', timestamp=None):
    area = area.upper()
    if area == 'A_US' and is_winter_time(timestamp):
        area = 'A_US_WINTER'
    return TIMEZONE_OFFSET.get(area, -7)


def day_utc_begin_with_timezone(utc_day=None, area='A_US'):
    """
    获取指定时区的天开始UTC时间
    :param utc_day: datetime.datetime with UTC
    :param area: 大区
    :return: area_day_start_with_utc
    """
    if not utc_day:
        utc_day = timezone.now()

    if not isinstance(utc_day, datetime):
        raise TypeError('Param `utc_day` type error.')

    if utc_day.tzinfo != utc:
        raise ValueError('Param `utc_day` timezone info must be "UTC"')

    offset = get_perfect_timezone_offset(area)
    area_utc_day = utc_day + timedelta(hours=offset)
    area_day_start = area_utc_day.replace(hour=0, minute=0, second=0, microsecond=0)
    return area_day_start - timedelta(hours=offset)


def month_utc_begin_with_timezone(utc_day=None, area='A_US'):
    """
    获取指定时区的月开始UTC时间
    :param utc_day: datetime.datetime with UTC
    :param area: 大区
    :return: area_month_start_with_utc
    """
    if not utc_day:
        utc_day = timezone.now()

    if not isinstance(utc_day, datetime):
        raise TypeError('Param `utc_day` type error.')

    if utc_day.tzinfo != utc:
        raise ValueError('Param `utc_day` timezone info must be "UTC"')

    offset = get_perfect_timezone_offset(area)
    area_utc_day = utc_day + timedelta(hours=offset)
    month_start = area_utc_day.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return month_start - timedelta(hours=offset)


def month_utc_begin_end_with_timezone(utc_day=None, area='A_US'):
    """
    获取指定时区的月开始UTC时间和月结束UTC时间
    :param utc_day: datetime.datetime with UTC
    :param area: 大区
    :return: area_month_start_with_utc
    """
    if not utc_day:
        utc_day = timezone.now()
    area_utc_month_start = month_utc_begin_with_timezone(utc_day, area)

    offset = get_perfect_timezone_offset(area)
    utc_month_start = area_utc_month_start + timedelta(hours=offset)
    next_month = utc_month_start
    while True:
        next_month += timedelta(days=1)
        if next_month.day == utc_month_start.day:
            break

    area_utc_mont_end = next_month - timedelta(hours=offset)
    return area_utc_month_start, area_utc_mont_end


def get_area_date_str_for_now(area='A_US'):
    """
    获取当前时间大区日期
    :param area:
    :return: 日期字符串，形如：2020-11-20
    """
    timestamp = time.time()
    offset = get_perfect_timezone_offset(area, timestamp)
    date_time = datetime.fromtimestamp(timestamp, tz=utc)
    area_date = date_time + timedelta(hours=offset)
    area_date = area_date.replace(hour=0, minute=0, second=0, microsecond=0)
    return area_date.strftime('%Y-%m-%d')


def get_month_date_str_for_now(area='A_US'):
    """
    获取当前时间大区月份日期
    :param area: 月份日期字符串，形如：2020-11
    :return:
    """
    area_date_str = get_area_date_str_for_now(area)
    return area_date_str[:-3]


def get_day_hour_range_with_utc(area_date_str=None, area='A_US'):
    """
    获取天小时范围
    :param area_date_str: 大区日期字符串，格式：%Y-%m-%d
    :param area: 大区
    :return: utc_day_start, hours (一天中的小时数，一般为24小时，美国切换冬令时当天为25小时，美国切换夏令时当天为23小时)
    """
    if area not in TIMEZONE_OFFSET:
        area = 'A_US'

    if not area_date_str:
        area_date_str = get_area_date_str_for_now(area)
    try:
        area_date = datetime.strptime(area_date_str, '%Y-%m-%d')
    except:
        return []

    _tz = LIVEME_AREA_TIMEZONE[area]
    _tz = pytz.timezone(_tz)
    area_date = area_date.replace(tzinfo=_tz)
    utc_date = area_date.astimezone(utc)

    hours_offset = 24
    if area == 'A_US':
        # 美国大区，区分冬令时和夏令时
        us_start, us_end = get_us_dst_range(area_date.year)
        area_date_end = area_date + timedelta(days=1)
        is_start_winter = False
        # 夏令时
        if us_start < area_date < area_date_end < us_end:
            pass
        # 冬切夏
        elif area_date < us_start < area_date_end < us_end:
            is_start_winter = True
            hours_offset = 23
        # 夏切冬
        elif us_start < area_date < us_end < area_date_end:
            hours_offset = 25
        # 冬令时
        else:
            is_start_winter = True

        if is_start_winter:
            tz_winter = LIVEME_AREA_TIMEZONE['A_US_WINTER']
            tz_winter = pytz.timezone(tz_winter)
            area_date_winter = area_date.replace(tzinfo=tz_winter)
            utc_date = area_date_winter.astimezone(utc)

    return utc_date, utc_date + timedelta(hours=hours_offset)


def get_month_range_with_utc(month_date_str=None, area='A_US'):
    """
    获取指定大区的月时间范围（UTC时间）
    :param month_date_str: 月份日期字符串
    :param area:
    :return: utc_month_first_day_start, utc_next_month_first_day_start, month_day_range_dict
        形如：datetime.datetime(2020, 3, 1, 8, 0, tzinfo=<UTC>), datetime.datetime(2020, 4, 1, 7, 0, tzinfo=<UTC>),
             {1: (datetime.datetime(2020, 3, 1, 8, 0, tzinfo=<UTC>), datetime.datetime(2020, 3, 2, 8, 0, tzinfo=<UTC>)),
              2: (datetime.datetime(2020, 3, 2, 8, 0, tzinfo=<UTC>), datetime.datetime(2020, 3, 3, 8, 0, tzinfo=<UTC>)),
              ...}

    """
    if area not in TIMEZONE_OFFSET:
        area = 'A_US'

    if not month_date_str:
        month_date_str = get_month_date_str_for_now(area)
    try:
        area_month = datetime.strptime(month_date_str, '%Y-%m')
    except:
        return []

    area_month_start = area_month
    area_next_month_start = base_offset_month_first_day(area_month_start, month_offset=1, time_begin=True)

    month_day_range = []
    area_day_index = area_month_start
    while area_day_index < area_next_month_start:
        _day_start, _day_end = get_day_hour_range_with_utc(area_day_index.strftime('%Y-%m-%d'), area)
        month_day_range.append((_day_start, _day_end))
        area_day_index += timedelta(days=1)
    month_day_range_dict = {day_num: day_range for day_num, day_range in enumerate(month_day_range, start=1)}

    return month_day_range[0][0], month_day_range[-1][1], month_day_range_dict
