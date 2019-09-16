from django.db import models


class Question(models.Model):
    author = models.CharField(max_length=50)
    question_title = models.CharField(max_length=50)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    question_hit = models.PositiveIntegerField(default=0) # 음수를 다루고 싶지 않으면 사용 Positive

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_title = models.CharField(max_length=50)
    choice_text = models.CharField(max_length=200)
    vote = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Comment(models.Model):
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_body = models.CharField(max_length=200) # 댓글 내용
    comment_user = models.CharField(max_length=50)
    comment_password = models.CharField(max_length=50)

    def __str__(self):
        return self.comment_body

    class Meta:
        ordering=['id']

