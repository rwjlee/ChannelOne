from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=256)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def join_dt(self):
        return datetime.strftime(self.created_at, '%B %d, %Y')

class BillItem(models.Model):
    description = models.CharField(max_length=64)
    amount = models.FloatField()

    user = models.ForeignKey(User, related_name='bills', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
