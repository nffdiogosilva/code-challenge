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
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.
    """
    # serializer_class = DailyPriceSerializer
    queryset = DailyPrice.objects.all()

    def list(self, request):
        serializer = QuerySerializer(data=request.query_params)
        
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            qs = DailyPrice.objects.filter(created_at__gte=start_date, created_at__lte=end_date)

            if 'company' in serializer.validated_data:
                qs = qs.filter(company__ticker=serializer.validated_data['company'])
            
            return Response(DailyPriceSerializer(qs, many=True).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecommendationViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.
    """
    # serializer_class = DailyPriceSerializer
    queryset = Recommendation.objects.all()

    def list(self, request):
        serializer = QuerySerializer(data=request.query_params)
        
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']
            qs = Recommendation.objects.filter(daily_price__created_at__gte=start_date, daily_price__created_at__lte=end_date)

            #if 'company' in serializer.validated_data:
            #    # TODO: get company id
            #    qs = qs.filter(daily_price__company_id=)

            # import pdb ; pdb.set_trace()
            return Response(RecommendationSerializer(qs, many=True).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
