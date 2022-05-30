from urllib import response

from django.shortcuts import render
from django.http import FileResponse, HttpRequest, HttpResponse, JsonResponse

from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework import viewsets

from midi_harmony_transfer.settings import BASE_DIR
from .serializers import firstappSerializer
from .models import midi_data

from django.views.decorators.csrf import csrf_exempt

from firstapp.algo import *
import json

from django.conf.urls.static import static

class firstappView(viewsets.ModelViewSet):
    serializer_class = firstappSerializer
    queryset = midi_data.objects.all()

@csrf_exempt
def main(request):
    #handle request
    res_body = None
    
    try:
        #Verify which file we want to use
        upload1 = request.FILES.get('upload1')
        upload2 = request.FILES.get('upload2')

        #midi_convert = request.FILES.get('midi_convert')
        res_body = request.body
    except Exception as e:
        pass

    if 'init' in str(res_body):
        upload1 = None
        upload2 = None
        upload_init = None
        try:
            midi_harm_transfer().terminator()
        except:
            pass
        return HttpResponse('backend is alive')
    
    if len(request.FILES) == 1:
        
        #upload1 = request.FILES.get('upload1')
        #upload2 = request.FILES.get('upload2')

        if upload1 != None:
            upload_init = midi_harm_transfer(upload1=upload1)
            value = 0

        elif upload2 != None:
            upload_init = midi_harm_transfer(upload2=upload2)
            value = 1

        #dist = distribution
        dist_df = upload_init.dist(midi=value)
        dist_df = dist_df.set_index('notes')
        dist_json = dist_df.to_json()
        dist_json = json.loads(dist_json)
        print(value)
        print(upload_init.key(value)[0])
        print(upload_init.key(value))
        key_json = f'{{"key": "{upload_init.key(value)[0]}"}}'
        key_json = json.loads(key_json)
        key2_json = f'{{"key2": "{upload_init.key(value)[1]}"}}'
        key2_json = json.loads(key2_json)
        
        tempo_json = f'{{"tempo": "{upload_init.tempo(value)}"}}'
        tempo_json = json.loads(tempo_json)

        time_length_json = f'{{"time_length": "{upload_init.time_length(value)}"}}'
        time_length_json = json.loads(time_length_json)
        
        velocity_json = upload_init.velocity(value)

        all_json = []
        all_json.append(dist_json)
        all_json.append(key_json)
        all_json.append(key2_json)
        all_json.append(tempo_json)
        all_json.append(time_length_json)
        all_json.append(velocity_json)

        return JsonResponse(all_json, safe=False)

        # elif midi_convert != None:
        #     #main_path = default_storage.save(str(midi_convert), ContentFile(midi_convert.read()))
        #     #midi_convert = os.path.join(settings.MEDIA_ROOT, main_path)

        #     #FluidSynth().midi_to_audio(str(BASE_DIR) + "\\" + str(midi_convert), str(BASE_DIR) + "\\" + 'audio.mp3')
        #     return HttpResponse('pass')

        

    if len(request.FILES) == 2:
        print('run')
        if request.FILES.get('upload1') != None and request.FILES.get('upload1') != None:
            print('transfering')

            midi_harm_transfer(upload1, upload2).dist_matching()
            
        
            return HttpResponse('s')

    if 'progress' in str(res_body):
        if 'noprogress' in str(res_body):
            print('cancelled')
            midi_harm_transfer().terminator()
            f = open(str(BASE_DIR) + str("\progress.txt"), "w")
            f.write(str(0))
            f.close()
            return HttpResponse('cancelled')
        else:
            

            f = open(str(BASE_DIR) + str("\progress.txt"), "r")
            progress = f.read()
            f.close()
            return HttpResponse(progress)

    if 'download_request' in str(res_body) or request.method == 'GET':
        outputmidi = str("output.mid")
        f = open(outputmidi, "rb")
        response = FileResponse(f)

        return response
    
    else:
        
        return HttpResponse('undefined')


class DataListView(ListAPIView):
    queryset=midi_data.objects.all()
    serializer_class=firstappSerializer

class DataDetailView(RetrieveAPIView):
    queryset=midi_data.objects.all()
    serializer_class=firstappSerializer
