from django.contrib.auth import get_user_model

from django.contrib.contenttypes.models import ContentType

from rest_framework.fields import SerializerMethodField
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.serializers import ModelSerializer,ValidationError

from accounts.api.serializers import UserDetailSerializer
from comments.models import Comment

def create_comment_serializer(model_type="post",slug=None,parent_id=None,user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                "id",
                "content",
                "timestamp",
            ]
        def __init__(self,*args,**kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count()==1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args,**kwargs)
        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count()!=1:
                raise ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count()!=1:
                raise ValidationError("This is not a slug for this content type")
            return data
        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                main_user= user
            else:
                main_user = get_user_model().objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(model_type=model_type,
                                                           slug=slug,
                                                           user=user,
                                                           content=content,
                                                           parent_obj=parent_obj,
                                                           )
            return comment
    return CommentCreateSerializer


class CommentListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name="comments-api:thread"
    )
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            "url",
            "id",
            "content",
            "reply_count",
            "timestamp",
        ]
    def get_reply_count(self,obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

class CommentChildSerializer(ModelSerializer):
    user  = UserDetailSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "content",
            "timestamp",

        ]

class CommentDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    reply_count = SerializerMethodField()
    replies = SerializerMethodField()
    content_object_url = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            # "content_type",
            # "object_id",
            "content",
            "timestamp",
            "reply_count",
            "replies",
            "content_object_url"
        ]
        read_only_fields = [
            # "content_type",
            # "reply_count",
            "object_id",
            "replies",
                ]
    def get_content_object_url(self,obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None
    def get_replies(self,obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(),many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0




class CommentEditSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "content",
            "timestamp",
        ]
