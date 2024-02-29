from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# database table name = user_level      &     Fields
class User_Level(models.Model):
    level_id = models.AutoField(primary_key=True)
    level_name = models.CharField(max_length=20, default=None, blank=True, null=True)

    def __str__(self):
        # this code shows the output in the admin panel
        return '{} {} '.format(self.level_name, self.level_id)


# database table name = region      &     Fields
class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_txt = models.CharField(max_length=100, default=None, blank=True, null=True)
    region_code = models.CharField(max_length=100, default=None, blank=True, null=True)
    priority = models.IntegerField(default=None, blank=True, null=True)

    def __str__(self):
        # this code shows the output in the admin panel
        return '{} {} {} {} '.format(self.region_txt, self.region_id, self.region_code, self.priority)


# database table name = depot      &     Fields
class Depot(models.Model):
    depot_id = models.CharField(primary_key=True, max_length=10)
    depot_txt = models.CharField(max_length=100, default=None, blank=True, null=True)
    deport_tel = models.CharField(max_length=100, default=None, blank=True, null=True)
    deport_image = models.CharField(max_length=500, default=None, blank=True, null=True)
    region = models.ForeignKey(Region, to_field='region_id', related_name="depot_set",
                               on_delete=models.CASCADE)
    priority = models.BooleanField(default=True)
    sortid = models.BooleanField(default=True)

    def __str__(self):
        # this code shows the output in the admin panel
        return '{} {} {} {}  '.format(self.depot_txt, self.deport_tel, self.region_id, self.priority)


# database table name = user      &     Fields
class User(AbstractUser):
    status = models.BooleanField(default=True)
    region = models.ForeignKey(Region, to_field='region_id', related_name="user_set", on_delete=models.CASCADE)
    depot = models.ForeignKey(Depot, to_field='depot_id', related_name="user_set", on_delete=models.CASCADE)
    user_level = models.ForeignKey(User_Level, to_field='level_id', related_name="user_set",
                                   on_delete=models.CASCADE)

    def __str__(self):
        # this code shows the output in the admin panel
        return '{} {} '.format(self.username, self.email)


# database table name = document      &     Fields
class Document(models.Model):
    document_id = models.AutoField(primary_key=True)
    document_type = models.CharField(max_length=3, default=None, blank=True, null=True)
    internal_doc_no = models.CharField(max_length=500, default=None, blank=True, null=True)
    storage_location = models.CharField(max_length=20, default=None, blank=True, null=True)
    document_date = models.CharField(max_length=15, default=None, blank=True, null=True)
    case_no = models.CharField(max_length=100, default=None, blank=True, null=True)
    court = models.CharField(max_length=500, default=None, blank=True, null=True)
    var_text1 = models.CharField(max_length=50, default=None, blank=True, null=True)
    var_text2 = models.CharField(max_length=50, default=None, blank=True, null=True)
    var_text3 = models.CharField(max_length=50, default=None, blank=True, null=True)
    var_text4 = models.CharField(max_length=50, default=None, blank=True, null=True)
    var_text5 = models.CharField(max_length=50, default=None, blank=True, null=True)
    var_text6 = models.CharField(max_length=50, default=None, blank=True, null=True)
    var_text7 = models.CharField(max_length=100, default=None, blank=True, null=True)
    var_text8 = models.CharField(max_length=100, default=None, blank=True, null=True)
    operation = models.CharField(max_length=100, default=None, blank=True, null=True)
    loadingCost = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    packingCost = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    landing_charge = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    other_fines = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    totsale = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    time = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=15, default=None, blank=True, null=True)
    trasferPostDate = models.DateField(default=None, blank=True, null=True)
    trasferSavedDate = models.DateField(default=None, blank=True, null=True)
    printed = models.IntegerField(default=None, blank=True, null=True)

    def __str__(self):
        # this code shows the output in the admin panel
        return '{} {} {} {}  '.format(self.document_type, self.document_date, self.totsale, self.case_no)


# database table name = master_data      &     Fields
class Master_Data(models.Model):
    material_no = models.AutoField(primary_key=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    girth = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    reduced_volume = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    time = models.TimeField(default=timezone.datetime(1970, 1, 1, 9, 42, 11, microsecond=0))
    visible_material_no = models.CharField(max_length=100, default=None, blank=True, null=True)
    qr_id = models.CharField(max_length=12, default=None, blank=True, null=True)
    category = models.CharField(max_length=100, default=None, blank=True, null=True)
    timber_class = models.CharField(max_length=100, default=None, blank=True, null=True)
    specis = models.CharField(max_length=100, default=None, blank=True, null=True)
    active = models.IntegerField(default=None, blank=True, null=True)
    lot_no = models.CharField(max_length=100, default=None, blank=True, null=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    value_grade = models.CharField(max_length=10, default=None, blank=True, null=True)
    value_price = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    transCost = models.DecimalField(max_digits=10, decimal_places=2, default=None, blank=True, null=True)
    doc_date = models.DateField(default=None, blank=True, null=True)
    gradeInCoupe = models.CharField(max_length=5, default=None, blank=True, null=True)
    soldGrade = models.CharField(max_length=5, default=None, blank=True, null=True)
    workingSheetNo = models.CharField(max_length=100, default=None, blank=True, null=True)
    auctionLotSheetNo = models.CharField(max_length=100, default=None, blank=True, null=True)
    percentage = models.DecimalField(max_digits=10, max_length=10, decimal_places=2, default=None, blank=True,
                                     null=True)
    yiel_d = models.DecimalField(max_digits=10, max_length=10, decimal_places=2, default=None, blank=True, null=True)
    logType = models.CharField(max_length=100, default=None, blank=True, null=True)
    # Foreign keys: User, Region, Depot, UserLevel
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    region = models.ForeignKey(Region, to_field='region_id', related_name="master_data_set", on_delete=models.CASCADE)
    depot = models.ForeignKey(Depot, to_field='depot_id', related_name="master_data_set", on_delete=models.CASCADE)

    def __str__(self):
        # this code shows the output in the admin panel
        return '{} {} {} {}  '.format(self.material_no, self.volume, self.user, self.visible_material_no, self.qr_id,
                                      self.value_price)


# database table name = movement      &     Fields
class Movement(models.Model):
    material_no = models.IntegerField(primary_key=True)
    movement = models.IntegerField(default=None, blank=True, null=True)
    old_ref_no = models.CharField(max_length=20, default=None, blank=True, null=True)
    new_ref_no = models.CharField(max_length=20, default=None, blank=True, null=True)
    bin = models.CharField(max_length=20, default=None, blank=True, null=True)
    time = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=20, default=None, blank=True, null=True)
    document_no = models.CharField(max_length=20, default=None, blank=True, null=True)
    valueGrade = models.CharField(max_length=20, default=None, blank=True, null=True)

    def __str__(self):
        # this code shows the output in the admin panel
        return '{} {} {} {} {} {}  '.format(self.material_no, self.movement, self.document_no, self.user,
                                            self.old_ref_no, self.new_ref_no)


# database table name = modify_reason   &   Fields
# this table is used to add reasons to modify QR ID
class Modify_Reason(models.Model):
    reason_id = models.AutoField(primary_key=True)
    reason = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log = models.ForeignKey(Master_Data, on_delete=models.CASCADE)

    def __str__(self):
        # this code shows the output in the admin panel
        return '{} {} {}  '.format(self.reason_id, self.user, self.log)


# database table name = working_sheet_log   &   Fields
# this table is used to keep track of searched logs
class Working_Sheet_Log(models.Model):
    ws_id = models.AutoField(primary_key=True)
    lot_id = models.CharField(max_length=255, default=None)
    time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #log = models.ForeignKey(Master_Data, on_delete=models.CASCADE)
    log_list = models.TextField(null=False, default=None)


    def __str__(self):
        # this code shows the output in the admin panel
        return '{} {} {}  '.format(self.ws_id, self.user, self.log)
