from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    image = models.CharField(max_length=150)
    type = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Chat(models.Model):
    chat_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    created_at = models.DateTimeField(auto_now_add=True)
    current_mutation = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50)
    def __str__(self):
        return self.content

