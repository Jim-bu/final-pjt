from rest_framework import serializers
from .models import DepositBaseList, DepositOptionList, SavingBaseList, SavingOptionList


class DepositBaseListSerializer(serializers.ModelSerializer):
    class OptionForProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = DepositOptionList
            fields = '__all__'
            
    deposit_options = OptionForProductSerializer(many=True, read_only=True)

    class Meta:
        model = DepositBaseList
        fields = '__all__'


class DepositOptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOptionList
        fields = '__all__'


class SavingBaseListSerializer(serializers.ModelSerializer):
    class OptionForProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = SavingOptionList
            fields = '__all__'
    
    saving_options = OptionForProductSerializer(many=True, read_only=True)

    class Meta:
        model = SavingBaseList
        fields = '__all__'


class SavingOptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOptionList
        fields = '__all__'