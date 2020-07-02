from rest_framework import serializers

from .models import Company, DailyPrice, Recommendation


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class DailyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyPrice
        fields = '__all__'


class DailyPriceCompanyField(serializers.RelatedField):
    def to_representation(self, value):
        return f'DP ({value.pk}) Company: {value.company.ticker}'

class RecommendationSerializer(serializers.ModelSerializer):
    daily_price = DailyPriceCompanyField(read_only=True)
    
    class Meta:
        model = Recommendation
        fields = (
            'id',
            'created_at',
            'to_grade',
            'scalar',
            'daily_price',
        )


class QuerySerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)

    def validate(self, data):
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date must be bigger than start date")
        return data
