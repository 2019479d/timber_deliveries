from rest_framework import serializers
from .models import Region, Depot, User, Master_Data, Modify_Reason, Working_Sheet_Log


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['region_id', 'region_txt']


class DepotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depot
        fields = ['depot_id', 'depot_txt']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class MasterDataSerializer(serializers.ModelSerializer):
    # Add these lines to include nested serializers
    region = RegionSerializer()
    depot = DepotSerializer()
    user = UserSerializer()

    class Meta:
        model = Master_Data
        fields = ['material_no', 'length', 'girth', 'volume', 'reduced_volume', 'time', 'visible_material_no',
                  'qr_id', 'category', 'timber_class', 'specis', 'active', 'lot_no', 'sale_price', 'value_grade',
                  'value_price', 'transCost', 'doc_date', 'gradeInCoupe', 'soldGrade', 'workingSheetNo',
                  'auctionLotSheetNo', 'percentage', 'yiel_d', 'logType', 'user', 'region', 'depot']


class ModifyReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modify_Reason
        fields = '__all__'


class WorkingSheetLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Working_Sheet_Log
        fields = '__all__'


class MasterDataSerializerForWS(serializers.ModelSerializer):
    # Add these lines to include nested serializers
    class Meta:
        model = Master_Data
        fields = ['material_no']