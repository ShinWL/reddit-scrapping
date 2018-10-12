import requests
from bs4 import BeautifulSoup
import re
from comments.models import Post, Comment
class SubReddit(object):
	"""docstring for SubReddit"""
	url = ''
	posts = []
	comments = []
	more_comments_url = []
	counter = 0

	def __init__(self):
		super(SubReddit, self).__init__()

	def set_subreddit_url(self, url):
		self.url = url

	def get_current_page_HTML(self, page_num):
		headers = {'User-Agent': 'Mozilla/5.0'}
		page = requests.get(self.url, headers=headers)
		soup = BeautifulSoup(page.text, 'html.parser')
		for current_page_num in range(page_num):
			soup = BeautifulSoup(page.text, 'html.parser')
			next_button = soup.find("span", class_="next-button")
			if not next_button:
				return 'End of subreddit.'
				break
			next_page_link = next_button.find("a").attrs['href']
			# time.sleep(2)
			page = requests.get(next_page_link, headers=headers)
		return soup

	def get_posts(self, page_num):
		# self.posts = []
		# headers = {'User-Agent': 'Mozilla/5.0'}
		# page = requests.get(self.url, headers=headers)
		print(page_num)
		soup = self.get_current_page_HTML(page_num) #BeautifulSoup(page.text, 'html.parser')
		if soup == 'End of subreddit.':
			return 'Terminate.'
		for post in soup.find_all('div', class_='thing'):
			post_title = post.find('p', class_="title").text
			post_url = 'https://www.reddit.com' + (post.get('data-permalink'))
			self.posts.append({
				'post_title': post_title,
				'post_url': post_url 
			})
		return self.posts
	

	def get_comments(self, post_url):
		# comments = []
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
				self.more_comments_url.append(post_url+comment_id+'/')
		
		def recursively_get_replies(data, post_title, post_content):
			self.counter += 1
			print('comment counter:',self.counter)
			if re.search(r'[\w\.-]+@[\w\.-]+', data['body']):
				self.comments.append(
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
						self.more_comments_url.append(post_url+comment_id+'/')
					return
				recursively_get_replies(reply['data'], post_title, post_content)

		for thread in comment_threads:
			data = thread['data']
			recursively_get_replies(data, post_title, post_content)

	def get_more_comments(self):
		for comment_url in self.more_comments_url:
			self.get_comments(comment_url)
		self.more_comments_url = []

	def store_posts(self):
		# Post.objects.all().delete()
		for data in self.posts:
			is_created = len(Post.objects.filter(post_url=data['post_url']))
			if not is_created:
				post = Post.objects.create(
					post_title=data['post_title'],
					post_url=data['post_url']
				)
				post.save()


	def store_comments(self, post_url):
		# Comment.objects.all().delete()
		# Delete post if no matched comments
		if len(self.comments) == 0:
			post_to_be_deleted = Post.objects.filter(post_url=post_url)
			for post in post_to_be_deleted:
				post.delete()
			return
		# Else save comments
		def save_comments(post, user_name, comment_content):
			comment = Comment.objects.create(
					post=post,
					user_name=user_name,
					comment_content=comment_content
				)
			comment.save()

		for comment_data in self.comments:
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
		self.comments = []

	def __str__(self):
		return self.url



if __name__ == '__main__':
	x = SubReddit()
	x.set_subreddit_url('https://old.reddit.com/r/Yandex/')
	for i in range(4):
		content = x.get_posts(i + 1)
		if(content == 'Terminate.'):
			break
	# print(x.posts)
	s.store_posts()
	for post in x.posts:
		# print(post['post_url'])
		x.get_comments(post['post_url'])
		x.get_more_comments()
	print(x.comments)
	del x
