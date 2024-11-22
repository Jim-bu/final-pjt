from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


## 테스트용임. 수정 필요합니다.
@csrf_exempt
def submit_survey(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        return JsonResponse({'status': 'success', 'message': '응답이 저장되었습니다.'})

