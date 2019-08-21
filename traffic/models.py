from django.db import models
from django.utils import timezone

class Classroom(models.Model):
    teacher = models.CharField(unique=True, max_length=200)

    def __str__(self):
        return self.teacher


class Family(models.Model):
    family_number = models.IntegerField(default=0, db_index=True)

    def __str__(self):
        return str(self.family_number)


class Student(models.Model):
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    def __str__(self):
        return str(f"{self.first_name} {self.last_name}")


class Checkout(models.Model):
    checkout_time = models.DateTimeField(auto_now_add=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    is_walker = models.BooleanField()

    def __str__(self):
        return str(f"{self.checkout_time}, is_walker={self.is_walker}")
