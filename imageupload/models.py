from django.db import models

class Image(models.Model):
    #pic_name = models.CharField('pic_name',max_length = 50, null = True)
    photo = models.ImageField(null=True, blank=True)


"""class Meta:
    db_table='ImageStore'
"""
def __str__(self):
    return self.photo.name

#class