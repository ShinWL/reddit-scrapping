from django.db import models
from bs4 import BeautifulSoup
import requests
import re
import time

class Post(models.Model):
	post_title = models.TextField()
	post_url = models.URLField()
	post_content = models.TextField()
	time_created = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.post_title

class Comment(models.Model):
	post = models.ForeignKey(Post)
	user_name = models.CharField(max_length=30)
	comment_content = models.TextField()
	time_created = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.user_name


class ModelOps(object):
	"""docstring for ModelOps"""
	# posts_data = []
	matched_comments = []
	subreddit = ''

	def __init__(self):
		super(ModelOps, self).__init__()
	
	def set_subreddit(self, subreddit):
		self.subreddit = subreddit

	def get_current_page_HTML(self, page_num):
		headers = {'User-Agent': 'Mozilla/5.0'}
		page = requests.get(self.subreddit, headers=headers)
		for current_page_num in range(page_num):
			soup = BeautifulSoup(page.text, 'html.parser')
			next_button = soup.find("span", class_="next-button")
			if not next_button:
				return 'End of subreddit.'
				break
			next_page_link = next_button.find("a").attrs['href']
			time.sleep(2)
			page = requests.get(next_page_link, headers=headers)
		return soup


	def get_posts(self, page_num):
		# self.posts_data=[]
		obj_list = []
		soup = self.get_current_page_HTML(page_num)
		if(soup == 'End of subreddit.'):
			return []
		for post in soup.find_all('div', class_='thing'):
			post_title = post.find('p', class_="title").text
			post_url = 'https://old.reddit.com' + (post.get('data-permalink'))
			obj_list.append({
				'post_title': post_title,
				'post_url': post_url 
				})
		# self.posts_data = obj_list
		return obj_list

	def store_posts(self, posts_data):
		# Post.objects.all().delete()
		for data in posts_data:
			is_created = len(Post.objects.filter(post_url=data['post_url']))
			if not is_created:
				post = Post.objects.create(
					post_title=data['post_title'],
					post_url=data['post_url']
				)
				post.save()
		

	def get_comments(self, post_url):
		# db_posts = get_posts_from_database()
		# for post in db_posts:
		self.matched_comments = []
		headers = {'User-Agent': 'Mozilla/5.0'}
		page = requests.get(post_url, headers=headers)
		soup = BeautifulSoup(page.text, 'html.parser')
		comment_area = soup.find('div', class_='commentarea')
		all_comments = comment_area.find_all('div', class_='thing')
		post_title = soup.find('a', class_='title').text
		for comment in all_comments:
			user = comment.get('data-author')
			if user:
				content = comment.find('div', class_='md').get_text()
				if re.search(r'[\w\.-]+@[\w\.-]+', content):
					# content = comment.find('div', class_='md').find('p')
					obj = {
						'post_title': post_title,
						'user_name': user,
						'comment_content': content
					}
					self.matched_comments.append(obj)
			time.sleep(2)
		if len(self.matched_comments) == 0:
			post_to_be_deleted = Post.objects.filter(post_url=post_url)
			for post in post_to_be_deleted:
				post.delete()
		return self.matched_comments

	def store_comments(self, post_url):
		# Comment.objects.all().delete()
		def save_comments(post, user_name, comment_content):
			comment = Comment.objects.create(
					post=post,
					user_name=user_name,
					comment_content=comment_content
				)
			comment.save()

		for comment_data in self.matched_comments:
			post_filtered = Post.objects.filter(post_url=post_url)
			if not post_filtered:
				post_filtered = Post.objects.create(
					post_title=comment_data['post_title'],
					post_url=post_url
					)
				post_filtered.save()
				save_comments(post_filtered, comment_data['user_name'], comment_data['comment_content'])
				continue
			for post_data in post_filtered:
				save_comments(post_data, comment_data['user_name'], comment_data['comment_content'])
		

	# NOT IN USE #
	# def get_posts_from_database(self):
	# 	q = Post.objects.all()
	# 	obj = []
	# 	for post in q:
	# 		obj.append({
	# 			'post_title': post.post_title,
	# 			'post_url': post.post_url 
	# 		})
	# 	return obj
	# NOT IN USED
	# def get_comments_from_database(self):
	# 	q = Comment.objects.all()
	# 	obj = []
	# 	for comment in q:
	# 		obj.append({
	# 			'post_title': comment.post.post_title,
	# 			'user': comment.user_name,
	# 			'content': comment.comment_content
	# 		})
	# 	return obj