from django.db import models

# Create your models here.
class FixedEquipmentBase(models.Model):
    """固定设备基本信息"""
    id = models.BigAutoField(primary_key=True)
    mac = models.CharField(max_length=50)
    site = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    class Meta:
        managed = True
        db_table = 't_fixed_equipment_base'


class FixedEquipmentStatus(models.Model):
    """固定设备动态信息表"""
    id = models.BigAutoField(primary_key=True)
    mac = models.CharField(max_length=50)
    rec_time = models.DateTimeField()
    status = models.IntegerField()  # 0=nomal 1=有员工进入了不该进入的设备范围 2=员工在设备附近呆了超过规定的时长
    class Meta:
        managed = True
        db_table = 't_fixed_equipment_status'


class FixedEquipmentPermission(models.Model):
    """固定设备许可"""
    id = models.BigAutoField(primary_key=True)
    mac = models.CharField(max_length=50)
    user_title = models.CharField(max_length=50)
    class Meta:
        managed = True
        db_table = 't_fixed_equipment_permission'


class MobileDeviceBase(models.Model):
    """移动设备基本信息表"""
    id = models.BigAutoField(primary_key=True)
    mac = models.CharField(max_length=50)
    user_title = models.CharField(max_length=50)
    employee_id = models.BigIntegerField()
    class Meta:
        managed = True
        db_table = 't_mobile_device_base'


class MobileDeviceStatus(models.Model):
    """移动设备动态信息表"""
    id = models.BigAutoField(primary_key=True)
    mac = models.CharField(max_length=50)
    rec_time = models.DateTimeField()
    site = models.CharField(max_length=50)
    level = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    lat = models.CharField(max_length=50)
    class Meta:
        managed = True
        db_table = 't_mobile_device_status'


class Employee(models.Model):
    """员工基本信息表"""
    employee_id = models.BigAutoField(primary_key=True)
    employee_title = models.CharField(max_length=50)
    employee_name = models.CharField(max_length=50)
    contact_info = models.CharField(max_length=50)
    class Meta:
        managed = True
        db_table = 't_employee'

