from django.db import models

class User(models.Model):
    sex = models.CharField(max_length=120)
    nickname = models.CharField(max_length=120)
    profile_photo = models.URLField()
    birthday = models.DateField()

    def to_dict(self):
        return {
            'id': self.id,
            'sex': self.sex,
            'nickname': self.nickname,
            'profile_photo': str(self.profile_photo),
            'birthday': str(self.birthday),
        }


class Post(models.Model):
    title = models.CharField(max_length=120)
    post_body = models.TextField(default="text")
    like = models.ManyToManyField(User, related_name="likes")
    hate = models.ManyToManyField(User, related_name="hate")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'post_body': self.post_body,
            'like': list(self.like.values_list('id', flat=True).all()),
            'hate': list(self.hate.values_list('id', flat=True).all()),
        }

    
class comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments")
    user = models.ForeignKey(User, related_name="comments")
    text = models.TextField(default="comment")

    def to_dict(self):
        return {
            'id': self.id,
            'post': self.post.id,
            'user': self.user.id,
            'text': self.text,
        }