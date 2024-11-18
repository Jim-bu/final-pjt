from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def submit_survey(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)  # 사용자 응답 데이터 출력 (디버깅용)
        return JsonResponse({'status': 'success', 'message': '응답이 저장되었습니다.'})

