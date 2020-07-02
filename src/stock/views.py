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
    Daily Price List Endpoint that returns...
    """
    queryset = DailyPrice.objects.all()

    def list(self, request):
        serializer = QuerySerializer(data=request.query_params)
        
        if serializer.is_valid():
            if 'company' in serializer.validated_data:
                qs = qs.filter(company=serializer.validated_data['company'])

            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            qs = DailyPrice.objects.filter(created_at__gte=start_date, created_at__lte=end_date)

            return Response(DailyPriceSerializer(qs, many=True).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.
    """
    queryset = Recommendation.objects.all()

    def list(self, request):
        serializer = QuerySerializer(data=request.query_params)
        
        if serializer.is_valid():
            if 'company' in serializer.validated_data:
                qs = qs.filter(daily_price__company=serializer.validated_data['company'])

            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            qs = Recommendation.objects.filter(created_at__gte=start_date, created_at__lte=end_date)
            avg = qs.aggregate(Avg('scalar'))
            
            return Response([avg] + RecommendationSerializer(qs, many=True).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
