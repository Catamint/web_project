from django.shortcuts import render
from django.shortcuts import HttpResponse
from productApp.models import movie_base, jumbotron_base
import json

# Create your views here.
def home(request):
    piece_dict={'id':[],
                'name':[],
                'intro':[],
                'label':[],
                'year':[],
                'status':[],
                'pics':[]
                }

    for piece in jumbotron_base.objects.all():
        piece_dict['id'].append(str(piece.movie.id))
        piece_dict['name'].append(piece.movie.name)
        if len(piece.movie.inform) < 200:
            piece_dict['intro'].append(piece.movie.inform)
        else:
            piece_dict['intro'].append(piece.movie.inform[0:200]+'...')
        if piece.pic == '':
            piece_dict['pics'].append(piece.movie.photo.url)
        else:
            piece_dict['pics'].append(piece.pic.url)

    return render(request, "home.html", {
        'active_menu':'home',
        'piece_dict':json.dumps(piece_dict),
        'len_dict':len(piece_dict['name'])
    })
