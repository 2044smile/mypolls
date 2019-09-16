from django.db.models import F
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from polls.forms import QuestionForm, ChoiceForm, CommentForm
from polls.models import Question, Choice, Comment


def index(request):
    q = Question.objects.get_queryset().order_by('pub_date') # Question의 오브젝트 전부를 question_list에 저장
    paginator = Paginator(q, 3) # 한 페이지에 3개의 q 를 띄운다.
    page = request.GET.get('page') # request.GET 브라우저 주소줄에 표시된다. 이름이 page인
    question_list = paginator.get_page(page)
    return render(request, 'polls/index.html', {'q': q, 'question_list': question_list})


def comment(request):
    comment = Comment.objects.all().order_by('-id')
    paginator = Paginator(comment, 5)
    page = request.GET.get('page')
    comment = paginator.get_page(page)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.comment_date = timezone.now()
            c.save()
            return render(request, 'polls/comment.html', {'form': form, 'comment': comment})
    else:
        form = CommentForm()
    return render(request, 'polls/comment.html', {'form': form, 'comment': comment})


def comment_delete(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == 'POST':
        if comment.comment_password == request.POST['comment_password']:
            print('삭제')
            comment.delete()
            return redirect('polls:comment')
        else:
            return render(request, 'polls/comment_delete.html', {'comment':comment, 'error': '패스워드가 일치하지 않습니다.'})
    return render(request, 'polls/comment_delete.html', {'comment': comment})


def detail(request, pk):
    form = CommentForm() # CommentForm을 form 안에 넣는다.
    c = Comment.objects.all() # Comment 의 모든 object를 c에 넣는다, 나중에 context로 리턴해준다.
    q = Question.objects.prefetch_related('choice_set').get(id=pk) # 최적화방법
    if request.method == "POST": # CommentForm을 작성해서 POST로 들어오면
        Pform = CommentForm(request.POST) # CommentForm에 POST로 들어온 것들을 Pform 안에 넣고
        if Pform.is_valid(): # 유효성 검사를 한다
            Pform.save(commit=False) # DB에 바로 저장하지 않고
            Pform.comment_user = request.user.username # [작동안함]
            Pform.comment_date = timezone.now() # 현재 시간을 comment_date에 넣는다.
            Pform.question = q.question_text
            Pform.save() # DB에 적용시킨다.
            return redirect('polls:detail', pk) # 현재 페이지로 redirect 시킨다.
        else:
            return HttpResponse('유효하지 않은 데이터입니다.') # Form 데이터가 유효하지 않으면 출력
    else:
        return render(request, 'polls/detail.html', {'question': q, 'form': form, 'c': c}) # 함수의 끝으로 context들을 리턴


def vote(request, pk):
    question = get_object_or_404(Question, id=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.vote += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def results(request, pk):
    question = get_object_or_404(Question, id=pk)
    return render(request, 'polls/results.html', {'question': question})


def create(request):
    if request.method == 'POST': # form 에서 요청이 POST로 오면
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.author = request.user
            q.pub_date = timezone.now()
            q.save()
            return redirect('polls:index')
    else: # form 에서 요청이 GET으로 오면 아래 form 형식을 출력하여 사용자가 입력하게끔
        form = QuestionForm()
    return render(request, 'polls/create.html',{'form': form,})


def create_choice(request):
    q = Question.objects.all()
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('polls:index')
    else:
        form = ChoiceForm()
    return render(request, 'polls/create_choice.html',{'form': form, 'q': q })


def delete(request, pk): # if 의 결과가 나오지않는다 연구가 필요해보인다.
    q = Question.objects.get(id=pk)
    error = '본인이 작성한 글만 삭제할 수 있습니다.'

    if request.method == 'POST': # post로 들어오면  and request.user == q.author
        if request.user.username == q.author:
        # 현재 로그인 중인 유저와 글 작성자가 맞는지 확인 후 맞다면
            q.delete() # q 삭제
            return HttpResponseRedirect('/')
        else: # 같지 않다면
            return render(request, 'polls/delete.html', {'q': q, 'error': error}) # 에러발생