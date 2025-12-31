from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Employeer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    email=models.EmailField(max_length=1000,blank=True,null=True)
    cargo=models.CharField(max_length=50)
    foto=models.ImageField(upload_to='funcionarios',null=True,blank=True)
    Online=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
class Task(models.Model):
    titulo = models.CharField(max_length=1000)
    descricao = models.TextField()
    conclusao = models.DateField()
    inicio = models.DateTimeField(auto_now_add=True)
    completo = models.BooleanField(default=False)

    empregador = models.ForeignKey(
        Employeer,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    def __str__(self):
        return self.titulo
class TaskUpload(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='uploads'
    )
    file = models.FileField(upload_to="tasks/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload da task {self.task.id}"