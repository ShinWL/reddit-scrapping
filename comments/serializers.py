from rest_framework import serializers
from comments.models import Post, Comment
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['post_title', 'post_url', 'time_created']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'user_name', 'comment_content', 'time_created']