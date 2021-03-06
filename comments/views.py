from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from comments.models import Comment, Post, ModelOps#, get_posts_from_database, get_comments_from_database
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
# Create your views here.
from comments.DataOperation2 import SubReddit
import comments.main as main 
import comments.teststore as test 
from comments.serializers import PostSerializer, CommentSerializer
from rest_framework import generics
class PostListCreate(generics.ListCreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer

class CommentListCreate(generics.ListCreateAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

@api_view(['GET'])
def fetch_posts(request):
	subreddit = request.GET.get('subreddit', '')
	# page_num = int(request.GET.get('page', '1'))
	if subreddit:
		s = SubReddit()
		s.set_subreddit_url(subreddit)
		s.get_posts()
		del s
		return HttpResponse('Subreddit Done.')
		# return HttpResponse(posts_data)
		# return HttpResponse('POST DONE.')
		# return HttpResponse(subreddit + ' ' + str(page_num))
	return HttpResponse('Invalid Query')

@api_view(['GET'])
def start_scraping(request):
	reddit = request.GET.get('reddit', '')
	if reddit:
		main.get_subreddits(reddit)

@api_view(['GET'])
def start(request):
	test.start()
## NOT IN USE ##
# @api_view(['GET'])
# def fetch_comments(request):
# 	post_url = request.GET.get('post', '')
# 	if post_url:
# 		op = ModelOps()
# 		matched_comments = op.get_comments(post_url)
# 		op.store_comments(post_url)
# 		# return HttpResponse('COMMENT DONE.')
# 		return Response(matched_comments)
	# return HttpResponse('Invalid Query')

# NOT USED #
# @api_view(['GET'])
# def get_database_posts(request):
# 	return Response(ModelOps().get_posts_from_database())

# @api_view(['GET'])
# def get_database_comments(request):
# 	return Response(ModelOps().get_comments_from_database())