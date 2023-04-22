import base64

from django.shortcuts import render, redirect
from django.http import Http404
from web import models
from decimal import Decimal
import matplotlib.pyplot as plt
from io import BytesIO
import datetime

# Create your views here.
def load(request):
    '''封面'''
    return render(request, "web/load.html")

def login_page(request):
    """登录页"""
    return render(request, "web/login_page.html")

def login_check(request):
    """单击登录钮，跳转首页"""
    return render(request, "web/first_page.html")

def return_first(request):
    """单击返回钮，跳转首页"""
    return render(request, "web/first_page.html")

def return_supervise_home(request):
    """单击返回钮，跳转Supervise首页"""
    return redirect("/web/supervise_home")

def return_maintenance_home(request):
    """单击返回钮，跳转Maintenance首页"""
    return redirect("/web/maintenance_home")

def supervise_home(request):
    """单击Supervise链接，跳转Supervise页面，显示机器信息"""
    sql = "select A.id, A.mac,A.rec_time,A.status, B.site,B.level,B.lon,B.lat"
    sql += " from (select mac, max(rec_time) as rec_time,id,status from t_fixed_equipment_status group by mac) as A"
    sql += " left join t_fixed_equipment_base as B on A.mac=B.mac"
    sql = sql + " order by A.mac"

    # 查询结果
    rec_list = models.FixedEquipmentStatus.objects.raw(sql)

    context={
        "rec_list": rec_list
    }
    return render(request, "web/supervise_home.html", context)

def show_machine_detail(request):
    """单击了机器，跳转机器详细信息页"""
    try:
        mac = request.GET.get("mac")

        # 根据mac地址获取固定设备基本信息
        sql = "select * from t_fixed_equipment_base where mac=%s"
        paras = [mac]
        rec_base = models.FixedEquipmentBase.objects.raw(sql, tuple(paras))[0]
        # 根据mac地址获取固定设备动态信息
        sql2 = "select * from t_fixed_equipment_status where mac=%s order by rec_time desc"
        paras2 = [mac]
        rec_status = models.FixedEquipmentStatus.objects.raw(sql2, tuple(paras2))[0]
        # 根据mac地址获取具有许可的用户角色列表
        sql3 = "select * from t_fixed_equipment_permission where mac=%s"
        paras3 = [mac]
        permission_list = models.FixedEquipmentPermission.objects.raw(sql3, tuple(paras3))

        context = {
            "mac": mac,
            "site": rec_base.site,
            "level": rec_base.level,
            "lon": rec_base.lon,
            "lat": rec_base.lat,
            "rec_time": rec_status.rec_time,
            "status": rec_status.status,
            "permission_list": permission_list
        }
        return render(request, "web/machine_detail.html", context)
    except Exception as err:
        raise Http404("ERROR！")

def show_machine_history(request):
    """单击了历史记录，跳转机器历史信息页"""
    try:
        mac = request.GET.get("mac")

        # 根据mac地址获取全部动态信息
        sql = "select id, rec_time, status from t_fixed_equipment_status where mac=%s order by rec_time desc"
        paras = [mac]
        history_info_list = models.FixedEquipmentStatus.objects.raw(sql, tuple(paras))

        context = {
            "mac": mac,
            "history_info_list": history_info_list,
        }
        return render(request, "web/machine_history.html", context)
    except Exception as err:
        raise Http404("ERROR！")

def maintenance_home(request):
    """单击Maintenance链接，跳转Maintenance页面，显示机器信息"""
    sql0 = "select id, max(rec_time) from t_fixed_equipment_status"
    curr_time = models.FixedEquipmentStatus.objects.raw(sql0)[0].rec_time

    sql = "select A.id, A.mac,A.rec_time,A.status, B.site,B.level,B.lon,B.lat"
    sql += " from (select mac, max(rec_time) as rec_time,id,status from t_fixed_equipment_status group by mac) as A"
    sql += " left join t_fixed_equipment_base as B on A.mac=B.mac"
    sql = sql + " order by A.mac"

    # 查询结果
    rec_list = models.FixedEquipmentStatus.objects.raw(sql)

    context={
        "curr_time": curr_time,
        "rec_list": rec_list
    }
    return render(request, "web/maintenance_home.html", context)


def time_minus(request):
    """时间减"""
    curr_time = request.GET.get("curr_time")
    curr_time = datetime.datetime.strptime(curr_time, '%Y-%m-%d %H:%M:%S')

    sql0 = "select id, rec_time from t_fixed_equipment_status where rec_time<%s order by rec_time desc"
    paras0 = [curr_time]
    time_list = models.FixedEquipmentStatus.objects.raw(sql0, tuple(paras0))
    if len(time_list)>0:
        curr_time = time_list[0].rec_time

    sql = "select A.id, A.mac,A.rec_time,A.status, B.site,B.level,B.lon,B.lat"
    sql += " from (select mac, max(rec_time) as rec_time,id,status from (select * from t_fixed_equipment_status where rec_time<=%s) as D group by mac) as A"
    sql += " left join t_fixed_equipment_base as B on A.mac=B.mac"
    sql = sql + " order by A.mac"
    paras = [curr_time]

    # 查询结果
    rec_list = models.FixedEquipmentStatus.objects.raw(sql, tuple(paras))

    context={
        "curr_time": curr_time,
        "rec_list": rec_list
    }
    return render(request, "web/maintenance_home.html", context)


def time_add(request):
    """时间增"""
    curr_time = request.GET.get("curr_time")
    curr_time = datetime.datetime.strptime(curr_time, '%Y-%m-%d %H:%M:%S')

    curr_time_new = curr_time  + datetime.timedelta(seconds=1)  # 传入的时间少了毫秒部分，新时间至少增1秒

    sql0 = "select id, rec_time from t_fixed_equipment_status where rec_time>=%s order by rec_time"
    paras0 = [curr_time_new]
    time_list = models.FixedEquipmentStatus.objects.raw(sql0, tuple(paras0))
    if len(time_list)>0:
        curr_time = time_list[0].rec_time

    sql = "select A.id, A.mac,A.rec_time,A.status, B.site,B.level,B.lon,B.lat"
    sql += " from (select mac, max(rec_time) as rec_time,id,status from (select * from t_fixed_equipment_status where rec_time<=%s) as D group by mac) as A"
    sql += " left join t_fixed_equipment_base as B on A.mac=B.mac"
    sql = sql + " order by A.mac"
    paras = [curr_time]

    # search result
    rec_list = models.FixedEquipmentStatus.objects.raw(sql, tuple(paras))

    context={
        "curr_time": curr_time,
        "rec_list": rec_list
    }
    return render(request, "web/maintenance_home.html", context)


def show_employees_nearby(request):
    """Click a machine link to display the employees and icons near the machine"""
    try:
        R = 0.03
        mac = request.GET.get("mac")

        # Obtain the longitude and latitude of a fixed device based on the mac address
        sql = "select id, lon, lat from t_fixed_equipment_base where mac=%s"
        paras = [mac]
        rec_fixed_equip = models.FixedEquipmentBase.objects.raw(sql, tuple(paras))[0]
        fixed_lon = float(rec_fixed_equip.lon)
        fixed_lat = float(rec_fixed_equip.lat)
        min_lon = fixed_lon
        min_lat = fixed_lat
        max_lon = fixed_lon
        max_lat = fixed_lat

        # Last seen location for all mobile devices
        sql2 = "select id, mac, max(rec_time) as rec_time, site, level, lon, lat from t_mobile_device_status group by mac"
        mobile_status_list = models.MobileDeviceStatus.objects.raw(sql2)

        employee_list = []
        mobile_lons = []
        mobile_lats = []
        mobile_no = []
        for ms_rec in mobile_status_list:
            dis = get_distance_hav(Decimal(fixed_lat), Decimal(fixed_lon), Decimal(ms_rec.lat), Decimal(ms_rec.lon))
            # print(dis)

            if dis < R:
                sql3 = "select A.id, A.mac, A.rec_time, A.site, A.level, A.lon, A.lat, B.employee_id, C.employee_title, C.employee_name, C.contact_info"
                sql3 += " from (select id, mac, max(rec_time) as rec_time, site, level, lon, lat from t_mobile_device_status where id=%s) as A"
                sql3 += " left join t_mobile_device_base as B on A.mac=B.mac"
                sql3 += " left join t_employee as C on B.employee_id=C.employee_id"
                paras3 = [ms_rec.id]
                e_rec = models.MobileDeviceStatus.objects.raw(sql3,tuple(paras3))[0]
                employee_list.append(e_rec)
                mobile_lons.append(float(e_rec.lon))
                mobile_lats.append(float(e_rec.lat))

        if len(mobile_lons)>0:
            min_lon = min(min_lon, min(mobile_lons))
            max_lon = max(max_lon, max(mobile_lons))
            min_lat = min(min_lat, min(mobile_lats))
            max_lat = max(max_lat, max(mobile_lats))

        build_lons = [51.460535, 51.460498, 51.460933, 51.460916, 51.460296, 51.460341]
        build_lats = [-0.933273, -0.932576, -0.932527, -0.93224, -0.932311, -0.933295]

        min_lon = min(min_lon, min(build_lons))
        max_lon = max(max_lon, max(build_lons))
        min_lat = min(min_lat, min(build_lats))
        max_lat = max(max_lat, max(build_lats))

        # Scatter plot
        plt.figure(figsize=(10,10),dpi=100)
        plt.scatter([fixed_lon], [fixed_lat], color='r', s=50)
        plt.scatter(mobile_lons, mobile_lats, color='b', s=20)
        plt.scatter(build_lons, build_lats, color='k', s=30)

        for i in range(len(mobile_lons)):
            plt.annotate(str(i+1), xy=(mobile_lons[i], mobile_lats[i]), xytext=(mobile_lons[i]+0.00001, mobile_lats[i]+0.00001))

        plt.xlim([min_lon-0.0001, max_lon+0.0001])
        plt.ylim([min_lat-0.0001, max_lat+0.0001])
        plt.xlabel("longitude")
        plt.ylabel("latitude")
        buffer = BytesIO()
        plt.savefig(buffer)
        plot_data = buffer.getvalue()
        imb = base64.b64encode(plot_data)
        ims = imb.decode()
        img = "data:image/png;base64,"+ims

        context = {
            "mac": mac,
            "rec_list":employee_list,
            "img": img
        }
        return render(request, "web/employees_nearby.html", context)
    except Exception as err:
        print(err)
        raise Http404("ERROR！")


# Calculate geospatial distance from two points latitude and longitude
from math import sin, asin, cos, radians, fabs, sqrt

def hav(theta):
    s = sin(theta / 2)
    return s * s

def get_distance_hav(lat0, lng0, lat1, lng1):
    EARTH_RADIUS = 6371  # The average radius of the earth is about 6371km
    # Using haversine formula to calculate the distance between two points on a sphere
    # Latitude and longitude converted to radians
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)
    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))      # km
    return distance