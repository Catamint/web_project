from django.db import models
from django.utils import timezone, datetime_safe
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
# 关于电影信息的数据
class kind_base(models.Model):
    kind = models.CharField(max_length=50)
    def __str__(self):
        return self.kind
    class Meta:
        verbose_name = '类型'
        verbose_name_plural = '类型'

class movie_base(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    inform = models.TextField(verbose_name="简介")
    rate = models.FloatField(verbose_name="评分", blank=True, null=True, default=5.0)
    label = models.ManyToManyField(kind_base, verbose_name="标签", null=True, default=None)
    time_publish = models.DateField(max_length=20, default=timezone.now, verbose_name="上映时间")
    views = models.IntegerField(verbose_name="访问量", blank=True, null=True, default=0)
    photo = models.ImageField(upload_to='movie/', blank=True)
    showing = models.BooleanField(default=False, verbose_name="正在上映")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '电影'
        verbose_name_plural = '电影'

class review_base(models.Model):
    head = models.CharField(max_length=50, default='标题') #del
    # add time
    # add support
    # add review
    mark = models.FloatField(verbose_name="评分", blank=True, null=True, default=5.0)
    body = models.TextField(max_length=500, verbose_name="内容")
    user = models.ForeignKey(User, verbose_name="用户", related_name="review", null=True, on_delete=models.SET_NULL, default="")
    movie = models.ForeignKey(movie_base, verbose_name="电影", related_name="review", null=True, on_delete=models.CASCADE, default=None)
    time = models.DateTimeField(max_length=20, default=timezone.now, verbose_name="时间")
    def __str__(self):
        return "%s-%s"%(self.movie.name, self.id)
    class Meta:
        verbose_name = '短评'
        verbose_name_plural = '短评'

class picture_base(models.Model):
    name = models.CharField(max_length=50, default='剧照')
    pic = models.ImageField(upload_to='movie/')
    movie=models.ForeignKey(movie_base, verbose_name="电影", related_name="pictures", null=True, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return "%s (%s)"%(self.name, self.id)
    class Meta:
        verbose_name = '剧照'
        verbose_name_plural = '剧照'

class jumbotron_base(models.Model):
    movie = models.ForeignKey(movie_base, verbose_name="电影", related_name="jumbotron", on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='jumbotron/', blank=True, null=True, default=None)
    def __str__(self):
        return "%s (%s)"%(self.movie, self.id)
    class Meta:
        verbose_name = '海报'
        verbose_name_plural = '海报'

# 用户
class user_exp(models.Model):
    photo = ProcessedImageField(upload_to='user/', blank=True, default='static/img/default.jpg',
                            verbose_name='头像', processors=[ResizeToFill(600,600)],)
    favorite = models.ManyToManyField(movie_base, verbose_name="想看", blank=True, null=True, default=None)
    user = models.OneToOneField(User, verbose_name="用户", related_name="other", on_delete=models.CASCADE, default="")

# 关于订票的数据
class hall_base(models.Model):
    name=models.CharField(max_length=100, verbose_name="名称")
    total_seats=models.IntegerField(verbose_name="座位数")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '放映厅'
        verbose_name_plural = '放映厅'

class session_base(models.Model):
    movie=models.ForeignKey(movie_base, verbose_name="电影", related_name="session", on_delete=models.PROTECT)
    time=models.DateTimeField(max_length=20, default=timezone.now, verbose_name="时间")
    location=models.ForeignKey(hall_base, verbose_name="厅", on_delete=models.PROTECT, default="")
    ordered_seats=models.IntegerField(verbose_name="已订座位数", blank=True, null=True, default=0)
    charge=models.IntegerField(verbose_name="票价", blank=True, null=True)

    def __str__(self):
        return '%s %s %s' % (self.movie.name, self.location.name, self.time.strftime('%Y/%m/%d %H:%M'))
        # self.time.strftime()
    class Meta:
        verbose_name = '场次'
        verbose_name_plural = '场次'

class ticket_base(models.Model):
    user=models.ForeignKey(User, verbose_name="用户", related_name="tickets", on_delete=models.CASCADE, default="")
    seat=models.IntegerField(verbose_name="座号", blank=True, null=True)
    session=models.ForeignKey(session_base, verbose_name="场次", null=True, on_delete=models.SET_NULL, default=None)
    time_create=models.DateTimeField(max_length=20, default=timezone.now, verbose_name="下单时间")
    STATUS_CHOICES = [(-1,'已取消'), (0,'未生效'), (1,'待核销'), (2,'已核销')]
    status=models.IntegerField(verbose_name="状态", blank=True, null=True, default=0 ,choices=STATUS_CHOICES)
    # -1:已取消 0,'未生效' 1,'已生效'
    
    class Meta:
        verbose_name = '票'
        verbose_name_plural = '票'