from django.shortcuts import render,get_object_or_404
from .models import Post,Comment
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from . forms import EmailPostForm,CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
def post_list(request,tag_slug=None):
    object_list=Post.published.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        object_list=object_list.filter(tags__in=[tag])
    paginator=Paginator(object_list,3)
    page=request.GET.get('page')
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)

    return render(request,'blog/post/list.html',{'page':page,'posts':posts,'tag':tag})
def post_details(request,post):
    post=get_object_or_404(Post,slug=post,
                           status='publish',
                           )
    comments=post.comments.filter(active=True)
    new_comment= None
    print(request.method)
    print('hello hii bllq')
    if request.method=='POST':
        print("post request")
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            print("comment valid")
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.save()
    else:
        comment_form=CommentForm()
    post_tags_ids=post.tags.values_list('id',flat=True)
    similer_posts=Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similer_posts=similer_posts.annotate(same_tag=Count('tags')).order_by('-same_tag','-publish')[:4]
    return render(request,'blog/post/details.html',{'post':post,'comments':comments,'new_comment':new_comment,'comment_form':comment_form,'similer_posts':similer_posts})
def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id,status='publish')
    sent=False
    if request.method == 'POST':
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'chaudhary003@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent })
