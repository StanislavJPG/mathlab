from __future__ import annotations
from datetime import datetime

from rest_framework import serializers

from .models import Post
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(required=False)
    dislikes_count = serializers.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation["modified_at"]:
            representation["modified_at"] = datetime.fromisoformat(
                representation["modified_at"]
            )
        representation["created_at"] = datetime.fromisoformat(
            representation["created_at"]
        )
        return representation

    def validate(self, attrs):
        if len(attrs["comment"]) >= 15:
            return attrs
        raise serializers.ValidationError("Length must be more than 15")

    def create(self, validated_data):
        post = Post.objects.select_related("user").get(pk=validated_data["post"].id)
        user = self.context["request"].user
        return Comment.objects.create(
            comment=validated_data["comment"], post=post, user=user
        )


# class categoriesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = categories
#         fields = ('categories_name',)


class PostSerializer(serializers.ModelSerializer):
    comments_quantity = serializers.IntegerField(required=False)
    likes = serializers.IntegerField(required=False)
    dislikes = serializers.IntegerField(required=False)

    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {
            "post_likes": {"required": False},
            "post_dislikes": {"required": False},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["created_at"] = datetime.fromisoformat(
            representation["created_at"]
        )
        representation["modified_at"] = datetime.fromisoformat(
            representation["modified_at"]
        )
        representation["categories"]: list = instance.get_foo_categories()
        return representation

    def validate(self, attrs):
        if (
            len(self.context["requested_categories"]) > 4
            or len(self.context["requested_categories"]) < 1
        ):
            raise serializers.ValidationError(
                "Менше однієї, або більше чотирьох категорій не приймається."
            )
        elif len(attrs["title"]) < 15 or len(attrs["content"]) < 15:
            raise serializers.ValidationError(
                "Довжина питання або опису питання не може бути меншою за 15 символів."
            )
        return attrs

    def create(self, validated_data):
        post = Post.objects.create(
            title=validated_data["title"],
            content=validated_data["content"],
            user=self.context["request"].user,
            categories=Post.represent_nums_to_categories(
                self.context["requested_categories"]
            ),
        )
        return post


class CommentLastActionsSerializer(serializers.ModelSerializer):
    """
    the only goal of using this serializer is some cases
    instead of default CommentSerializer
    it's reduce a quantity of database queries
    """

    post = PostSerializer()

    class Meta:
        model = Comment
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["created_at"] = datetime.fromisoformat(
            representation["created_at"]
        )
        representation["comm_id"] = representation["id"]
        representation["title"] = representation["comment"]
        return representation
