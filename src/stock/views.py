from django.db.models import Avg
from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Company, DailyPrice, Recommendation
from .serializers import CompanySerializer, DailyPriceSerializer, RecommendationSerializer, QuerySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class DailyPriceViewSet(viewsets.ViewSet):
    """
    Daily Price List Endpoint.
    You can query results through: start_date, end_date and companies parameters.
    """
    queryset = DailyPrice.objects.all()

    def list(self, request):
        serializer = QuerySerializer(data=request.query_params)
        
        if serializer.is_valid():
            qs = self.queryset

            if 'companies' in serializer.validated_data:
                qs = qs.filter(company__in=serializer.validated_data['companies'])

            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            qs = qs.filter(created_at__gte=start_date, created_at__lte=end_date)

            return Response(DailyPriceSerializer(qs, many=True).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationViewSet(viewsets.ViewSet):
    """
    Recommendation List Endpoint.
    You can query results through: start_date, end_date and companies parameters.
    """
    queryset = Recommendation.objects.all()

    def list(self, request):
        serializer = QuerySerializer(data=request.query_params)
        
        if serializer.is_valid():
            qs = self.queryset
            if 'companies' in serializer.validated_data:
                qs = qs.filter(daily_price__company__in=serializer.validated_data['companies'])

            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            qs = qs.filter(created_at__gte=start_date, created_at__lte=end_date)
            avg = qs.aggregate(Avg('scalar'))['scalar__avg']
            
            return Response([{'scalar_avg': avg}] + RecommendationSerializer(qs, many=True).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
