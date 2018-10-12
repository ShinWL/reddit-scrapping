import requests
from bs4 import BeautifulSoup
from comments.DataOperation import SubReddit
from comments.models import Post, Comment

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

def unique_list(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

def get_current_page_HTML(url):
	headers = {'User-Agent': 'Mozilla/5.0'}
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.text, 'html.parser')
	return soup

def get_subreddits(reddit):
	headers = {'User-Agent': 'Mozilla/5.0'}
	page = requests.get(reddit, headers=headers)
	soup = BeautifulSoup(page.text, 'html.parser')
	subreddits = []
	while True:
		for thing in soup.find_all('div', class_='thing'):
			subreddit_url = 'https://www.reddit.com/' + (thing.get('data-subreddit-prefixed'))
			subreddits.append(subreddit_url)
			subreddits = unique_list(subreddits)
			## start processing
			for sr in subreddits:
				post = []
				while True:
					bs = get_current_page_HTML(sr)
					for post in bs.find_all('div', class_='thing'):
						post_title = post.find('p', class_="title").text
						post_url = 'https://www.reddit.com' + (post.get('data-permalink'))
						posts.append({
							'post_title': post_title,
							'post_url': post_url 
						})
					store_posts(posts)
					### STORE COMMENT ###
					next_button = bs.find("span", class_="next-button")
					if not next_button:
						break
					next_page_link = next_button.find("a").attrs['href']
					bs = get_current_page_HTML(next_page_link)
			next_button = soup.find("span", class_="next-button")
			if not next_button:
				break
			next_page_link = next_button.find("a").attrs['href']
			page = requests.get(next_page_link, headers=headers)
			soup = BeautifulSoup(page.text, 'html.parser')
	return subreddits


if __name__ == '__main__':
	# reddit = input("Reddit: ")
	# page = input("Page: ")
	# if reddit:
	# 	baseURL = 'http://127.0.0.1:8000/api/fetch_post/?subreddit='+reddit+'.json&page=' + page
	# 	r = requests.get(baseURL)
	# 	print(reddit + ': DONE.')
	print(get_subreddits('https://old.reddit.com/hot/'))
