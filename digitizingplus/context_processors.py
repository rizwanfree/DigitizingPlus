from frontend.models import CompanyInfo

def company_info(request):
    try:
        company = CompanyInfo.objects.first()
    except CompanyInfo.DoesNotExist:
        company = None
    return {'company_info': company}