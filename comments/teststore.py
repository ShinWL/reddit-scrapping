import requests
import csv
import time
from bs4 import BeautifulSoup
import re
from comments.models import Post, Comment

def get_comments(post_url, more_comment, comments):
	headers = {'User-Agent': 'Mozilla/5.0'}
	r = requests.get(post_url + '.json', headers=headers)
	comment_threads = r.json()[1]['data']['children']
	post_title = r.json()[0]['data']['children'][0]['data']['title']
	post_content = r.json()[0]['data']['children'][0]['data']['url']
	# print(post_title)
	if len(comment_threads) == 0:
		return
	last_thread = comment_threads[len(comment_threads) - 1]
	if last_thread['kind'] == 'more':
		list_id = last_thread['data']['children']
		comment_threads.pop()
		for comment_id in list_id:
			more_comment.append(post_url+comment_id+'/')
	def recursively_get_replies(data, post_title, post_content):
		# self.counter += 1
		print('reply: '+data['body'])
		if re.search(r'[\w\.-]+@[\w\.-]+', data['body']):
			comments.append(
				{
				'post_title': post_title,
				'post_content': post_content,
				'user_name' : data['author'],
				'comment_content': re.findall(r'[\w\.-]+@[\w\.-]+', data['body'])
				})
		if data['replies'] == '':
			return
		replies = data['replies']['data']['children']
		for reply in replies:
			if reply['kind'] == 'more':
				list_id = reply['data']['children']
				for comment_id in list_id:
					more_comment.append(post_url+comment_id+'/')
				return
			recursively_get_replies(reply['data'], post_title, post_content)

	for thread in comment_threads:
		data = thread['data']
		recursively_get_replies(data, post_title, post_content)
def get_more_comments(more_comment, comments):
	for comment_url in more_comment:
		get_comments(comment_url, more_comment, comments)

def get_current_page_HTML(url):
	headers = {'User-Agent': 'Mozilla/5.0'}
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.text, 'html.parser')
	return soup

def store_comments(post_url, comments):
		# Comment.objects.all().delete()
		# Delete post if no matched comments
		if len(comments) == 0:
			post_to_be_deleted = Post.objects.filter(post_url=post_url)
			for post in post_to_be_deleted:
				post.delete()
			return
		# Else save comments
		def save_comments(post, user_name, comment_content):
			print(comment_content)
			comment = Comment.objects.create(
					post=post,
					user_name=user_name,
					comment_content=comment_content
				)
			comment.save()

		for comment_data in comments:
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
				post_data.post_content = comment_data['post_content']
				post_data.save()
				save_comments(post_data, comment_data['user_name'], comment_data['comment_content'])
def store_posts(posts_data):
	# Post.objects.all().delete()
	for data in posts_data:
		is_created = len(Post.objects.filter(post_url=data['post_url']))
		if not is_created:
			post = Post.objects.create(
				post_title=data['post_title'],
				post_url=data['post_url']
			)
			post.save()

def start():
	posts = []
	counter = 0
	bs = get_current_page_HTML('https://old.reddit.com/r/malaysia/')
	while True:
		for post in bs.find_all('div', class_='thing'):
			post_title = post.find('p', class_="title").text
			post_url = 'https://www.reddit.com' + (post.get('data-permalink'))
			posts.append({
				'post_title': post_title,
				'post_url': post_url 
			})
		store_posts(posts)
		### STORE COMMENT ###
		for post in posts:
			more_comment = []
			comments = []
			print('post:' + str(post))
			print()
			get_comments(post['post_url'], more_comment, comments)
			print(len(comments))
			get_more_comments(more_comment, comments)
			print(len(comments))
			store_comments(post['post_url'], comments) 
			print('post' + str(counter) + ' DONE.')
			counter += 1
		next_button = bs.find("span", class_="next-button")
		if not next_button:
			print('subreddit DONE.')
			break
		next_page_link = next_button.find("a").attrs['href']
		bs = get_current_page_HTML(next_page_link)

	# get_comments(posts[0])