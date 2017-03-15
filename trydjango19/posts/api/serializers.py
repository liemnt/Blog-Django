from rest_framework.fields import SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer

from accounts.api.serializers import UserDetailSerializer
from comments.api.serializers import CommentListSerializer, CommentDetailSerializer
from comments.models import Comment
from posts.models import Post


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "publish",

        ]


class PostDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    markdown = SerializerMethodField()
    url = HyperlinkedIdentityField(
        view_name="posts-api:detail",
        lookup_field="slug",
    )
    comments = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            "url",
            "id",
            "user",
            "title",
            "slug",
            "content",
            "markdown",
            "publish",
            "image",
            "comments",
        ]

    def get_markdown(self, obj):
        return obj.get_markdown()

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image
    def get_comments(self,obj):
        # content_type = obj.get_content_type
        # obj_id = obj.id
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentDetailSerializer(c_qs,many=True).data
        return comments


class PostListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="posts-api:detail",
        lookup_field="slug",
    )
    user = UserDetailSerializer(read_only=True)
    delete_url = HyperlinkedIdentityField(
        view_name="posts-api:delete",
        lookup_field="slug"
    )

    class Meta:
        model = Post
        fields = [
            "url",
            "user",
            "title",
            "content",
            "publish",
            "delete_url",
        ]
