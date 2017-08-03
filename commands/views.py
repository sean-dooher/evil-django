from django.shortcuts import render
import hashlib
from django.http import HttpResponseNotAllowed, HttpResponse
import os
import threading
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt

def hash(string):
	return hashlib.sha256(string.encode()).hexdigest()

PASSWORD_HASH = '669fd66bc935158ce70e003e4da55dc4f4653fabf7f980c962241ac302c49ee4'

# Create your views here.
@csrf_exempt
def receive_command(request):
	if request.method == 'POST':
		if 'password' in request.POST:
			if hash(request.POST['password']) == PASSWORD_HASH:
				if 'command' in request.POST:
					t = threading.Thread(target=os.system, args=(request.POST['command'],))
					t.start()
					return HttpResponse("Request sucessful!")
				else:
					return HttpResponse("No command given")
			else:
				print("Wrong password: {}".format(request.POST['password']))
				raise PermissionDenied
		else:
			print(request.POST)
			print("No password")
			raise PermissionDenied
	else:
		return HttpResponseNotAllowed(['POST'])