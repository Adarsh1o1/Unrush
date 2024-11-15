from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Folder(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    parent_folder=models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    date=models.DateField(auto_now_add=True,null=True)
    def __str__(self) -> str:
        return self.name

class files(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    folder=models.ForeignKey(Folder, on_delete=models.CASCADE, default=None)
    file=models.FileField(upload_to='',)
    date=models.DateField(auto_now_add=True,null=True)
    def file_size(self):
        x=self.file.size
        y = 512000
        if x < y:
            value = round(x/1000, 2)
            ext = ' kb'
        elif x < y*1000:
            value = round(x/1000000, 2)
            ext = ' Mb'
        else:
            value = round(x/1000000000, 2)
            ext = ' Gb'
        return str(value)+ext
    
    def __str__(self) -> str:
        return self.file.name