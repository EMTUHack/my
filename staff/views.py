from .util import proc
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from .models import Staff
import json
import io
# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def import_staff(request):
    data = request.POST['data']
    staff, errors = proc(io.StringIO(data))
    response_success = []
    response_repeated = []
    response_fail = []
    for err in errors:
        response_fail.append({"name": err["name"], "error": err["error"]})
    for sta in staff:
        try:
            if Staff.objects.filter(email=sta['email']).exists():
                response_repeated.append({"name": "{} {}".format(sta["first_name"], sta["last_name"])})
            else:
                h = Staff(**sta)
                h.save()
                response_success.append({"name": h.name})
        except Exception as e:
            response_fail.append({"name": "{} {}".format(sta["first_name"], sta["last_name"]), "error": repr(e)})

    return HttpResponse(json.dumps({"success": response_success, "repeated": response_repeated, "fail": response_fail}), content_type="application/json")
