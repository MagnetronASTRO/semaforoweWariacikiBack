import json
from rest_framework import viewsets, parsers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from OSMPythonTools.nominatim import Nominatim
import pandas as pd 
import geopandas as gpd
from shapely import Point
from .serializers import EventSerializer, CategorySerializer, ImageSerializer
from .models import Event, Category, Image


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        lat, long = self._get_lat_long_for_location(data['location'])
        data['latitude'] = lat
        data['longitude'] = long
        serializer = EventSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def _get_lat_long_for_location(self, location):
        nominatim = Nominatim()
        result = nominatim.query(location)
        as_json = result.toJSON()

        lat = as_json[0]['lat']
        long = as_json[0]['lon']
        return lat, long
    
    @action(methods=['GET'], detail=False, url_path=r'get_nearest_events/(?P<coords>([0-9]+\.[0-9]+,?)+)', url_name='get-nearest-sort')
    def get_nearest_event(self, request, coords):
        point = Point(coords.split(','))
        df = pd.DataFrame(list(Event.objects.all().values()))
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
        gdf['distance'] = gdf.distance(point)
        gdf.sort_values(by=['distance'], inplace=True)

        result_df = gdf.drop(['geometry'], axis=1)

        return Response(json.loads(result_df[:10].to_json(orient="records")), status.HTTP_200_OK)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
