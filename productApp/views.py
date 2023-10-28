from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, HttpResponse
from .models import movie_base, session_base, ticket_base, User, kind_base, review_base
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.core.paginator import Paginator
# Create your views here.

submenu_dict={'all': '全部电影', 'showing':'正在热映', 'highrate':'高分榜'}

def movie_by_submenu(submenu_id):
    if submenu_id == 'showing':
        return movie_base.objects.filter(showing=True)
    elif submenu_id == 'highrate':
        return movie_base.objects.order_by('-rate')
    else:
        return movie_base.objects.all()

def product(request, submenu_id):
    labels = kind_base.objects.all()
    movies = list(movie_by_submenu(submenu_id))
    filted = False
    # 按标签筛选
    if request.GET and request.GET.getlist('category'):
        filted = True
        category = set(request.GET.getlist('category'))
        movies = [movie for movie in movies if category & set([kind.kind for kind in movie.label.all()])]
    paginator = Paginator(movies, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'product.html', {
        'active_menu':'product',
        'active_submenu': submenu_id,
        'productName':submenu_dict[submenu_id],
        'movies_paged': page_obj,
        'labels' : labels,
        'filted': filted,
    })

def movie_view(request, movieid):
    movie = get_object_or_404(movie_base, id=movieid)
    sessions = []
    date = None
    dates = None

    # 按date属性分类
    if movie.showing:
        sessions = movie.session.all().order_by('time')
        date_sessions = {}
        for session in sessions:
            time = session.time
            if time:
                date_str = time.strftime("%Y-%m-%d")
                if date_str not in date_sessions:
                    date_sessions[date_str] = []
                date_sessions[date_str].append(session)
        dates=list(date_sessions.keys())
        if 'date' in request.GET:
            date=request.GET['date']
        else:
            date=dates[0]
        sessions=date_sessions[date]

    if request.method == "POST":
        comment = request.POST.get('comment')
        mark = int(request.POST.get('btnradio'))
        if len(comment) < 10:
            error = '评论至少在10字以上'
            return redirect('/m/movie/'+str(movieid)+'?error='+error+'#review_head')
        else:
            #存数据
            len_review = review_base.objects.filter(movie=movie).count()
            movie.rate = movie.rate * len_review/(len_review+1) + mark * 1/(len_review+1)
            movie.save()
            review_base.objects.create(mark=mark,body=comment,movie=movie,user=request.user)
            
            return redirect('/m/movie/'+str(movieid)+'#review_head')
    
    else:
        
        favorite = False
        if request.user.is_authenticated:
            favorite = movie in request.user.other.favorite.all()

        review_list = movie.review.all().order_by('-time')
        paginator = Paginator(review_list, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, 'movie.html', {
            'movie':movie,
            'pics':movie.pictures.all(),
            'labels':movie.label.all(),
            'reviews_paged':page_obj,
            'current_date':date,
            'dates':dates,
            'sessions': sessions,
            'is_favorite': favorite,
            'rate': "{:.1f}".format(movie.rate)
        })

def ordering_view(request, sessionid):
    session = get_object_or_404(session_base, id=sessionid)
    last_seats = int(session.location.total_seats) - int(session.ordered_seats)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        if request.user.is_authenticated == False:
            return redirect('/u/login/$?next=/m/ordering/'+sessionid)
        elif last_seats < quantity :
            return redirect('/m/movie/' + str(session.movie.id) + '?error_order=余票不足' + '#buy_ticket_head')
        else:
            session.ordered_seats += quantity
            session.save()
            for i in range(quantity):
                ticket = ticket_base(session=session, user=request.user, status=1)
                ticket.save()
            return render(request, 'orderSuccess.html', {
                'movie':session.movie,
                'session':session
            })
    else:
        if request.user.is_authenticated == False:
            return redirect('/u/login/$?next=/m/ordering/'+sessionid)
        return render(request, 'ordering.html', {
            'movie':session.movie,
            'session':session
        })

def ticket_view(request, ticketid):
    ticket = get_object_or_404(ticket_base, id=ticketid)
    session = ticket.session
    user = ticket.user
    if request.user != user:
        return redirect('/')
    else:
        return render(request, 'ticket.html', {
            'movie':session.movie,
            'session':session,
            'ticket':ticket
        })

def search_view(request):
    labels = kind_base.objects.all()
    if  request.method == 'GET': 
        q = request.GET.get('s_movie')
        if not q:
            return redirect('/m/products/all') 
        else:
            movies = movie_base.objects.filter(name__icontains=q)

            paginator = Paginator(movies, 8)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            return render(request, 'product.html', {
                'active_menu':'product',
                'active_submenu': 'search',
                'productName':'搜索结果(共'+ str(len(movies)) +'条)',
                # 'movies': movies,
                'labels' : labels,
                'movies_paged': page_obj,
            })
    else:
        return redirect('/')
    
def add_fav_view(request, movieid, action):
    if request.user.is_authenticated == False:
        return redirect('/u/login/$?next=/m/movie/'+movieid)
    
    movie = get_object_or_404(movie_base, id=movieid)
    if action == 'del':
        if movie in request.user.other.favorite.all():
            request.user.other.favorite.remove(movie)
    elif action == 'add':
        if movie not in request.user.other.favorite.all():
            request.user.other.favorite.add(movie)
    
    return redirect('/m/movie/'+str(movieid))

def del_fav_view(request, movieid):
    movie = get_object_or_404(movie_base, id=movieid)
    if movie in request.user.other.favorite.all():
        request.user.other.favorite.remove(movie)
    return redirect('/u/me/favorites')