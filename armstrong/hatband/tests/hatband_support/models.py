from django.db import models


class TestCategory(models.Model):
    name = models.CharField(max_length=255)


class TestArticle(models.Model):
    text = models.TextField()
    category = models.ForeignKey(TestCategory)
