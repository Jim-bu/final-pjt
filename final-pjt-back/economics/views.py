from rest_framework.decorators import api_view
from rest_framework.response import Response
from finance_recommendation.settings import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET
from .models import NewsList
from .serializers import NewsListSerializer
import requests


@api_view(['GET'])
def news_fetch_data(request):
    # Query parameter
    query = request.GET.get('query', '경제 주식')  # 기본 검색어: '경제'
    display = request.GET.get('display', 10)
    start = request.GET.get('start', 1)
    sort = request.GET.get('sort', 'date')

    # 네이버 API 요청
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    params = {
        "query": query,
        "display": display,
        "start": start,
        "sort": sort,
    }
    response = requests.get(url, headers=headers, params=params)

    # 데이터 처리
    data = response.json()
    items = data.get("items", [])
    saved_items = []

    for item in items:
        news_obj, created = NewsList.objects.update_or_create(
            title=item["title"],
            defaults={
                "originallink": item["originallink"],
                "link": item["link"],
                "description": item["description"],
                "pub_date": item["pubDate"],
            },
        )
        saved_items.append(news_obj)

    return Response({"message": "News fetched successfully.", "news_count": len(saved_items)})


@api_view(['GET'])
def news_get_data(request):
    news = NewsList.objects.all().order_by('-pub_date')
    serializer = NewsListSerializer(news, many=True)
    return Response(serializer.data)
