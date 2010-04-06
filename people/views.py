from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_list_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson

from django.contrib.auth.models import User

from fhpmwa.people.forms import UserForm

class HttpJsonResponse(HttpResponse):
    def __init__(self, content, mimetype=None, status=None, content_type='application/json', fields=None, is_ajax=True):
        if not is_ajax: content_type = 'text/plain'
        content = simplejson.dumps(content)
        return super(HttpJsonResponse, self).__init__(content=content, status=status, content_type=content_type)

def people_list(request):
    people = get_list_or_404(User.objects.filter(is_active=True).order_by('last_name'))
    data = []
    for person in people:
        data.append({
            'id': person.id,
            'username': person.username,
            'first_name': person.first_name,
            'last_name': person.last_name,
            'email': person.email,
            'matric_no': person.get_profile().matric_no,
            'zipcode': person.get_profile().zipcode,
            'mobile_device': person.get_profile().get_mobile_device(),
            'computer_os': person.get_profile().get_computer_os_display(),
            'photo_mini': person.get_profile().get_photo(45,45, opts=['crop',]),
            'photo_thumb': person.get_profile().get_photo(75,75, opts=['crop',]),
            'photo': person.get_profile().get_photo(320,415, opts=['upscale',])
        })
    return HttpJsonResponse(data, is_ajax=request.is_ajax())

def people_stats(request):
    people = get_list_or_404(User.objects.filter(is_active=True).order_by('last_name'))
    device_stats = {}
    os_stats = {}
    for person in people:
        device = person.get_profile().get_mobile_device()
        if device_stats.has_key(device):
            device_stats[device] = device_stats[device]+1
        else:
            device_stats[device] = 1

        os = person.get_profile().get_computer_os_display()
        if os_stats.has_key(os):
            os_stats[os] = os_stats[os]+1
        else:
            os_stats[os] = 1
    data = {
        'mobile_device': sorted(device_stats.iteritems(), key=lambda (k,v): (v,k), reverse=True),
        'computer_os': sorted(os_stats.iteritems(), key=lambda (k,v): (v,k), reverse=True),
    }
    return HttpJsonResponse(data, is_ajax=request.is_ajax())

def register(request):
    if request.method == 'GET':
        form = UserForm()
        return render_to_response('people/register.html', {'form': form}, context_instance=RequestContext(request))
    else:
        form = UserForm(request.POST, request.FILES)
        if not form.is_valid():
            error = 'The entered data was invalid.'
        else:
            # try:
            user = User.objects.create(
                username = slugify(request.POST.get('first_name') + request.POST.get('last_name')).replace('-',''),
                first_name = request.POST.get('first_name'),
                last_name = request.POST.get('last_name'),
                email = request.POST.get('email'),
            )
            user.set_password(request.POST.get('password'))
            user.save()
            profile = user.get_profile()
            if request.FILES.get('photo', None):
                profile.photo = request.FILES['photo']
            profile.matric_no = request.POST.get('matric_no', '')
            profile.zipcode = request.POST.get('zipcode', '')
            profile.mobile_device = request.POST.get('mobile_device', 0)
            profile.mobile_device_other = request.POST.get('mobile_device_other', '')
            profile.computer_os = request.POST.get('computer_os', 0)
            profile.save()
            return HttpResponseRedirect(reverse('people_register_done'))
            # except IntegrityError:
            #     error = 'The username is already taken. Please choose another one.'
        
        return render_to_response('people/register.html', {'form': form, 'error': error}, context_instance=RequestContext(request))

