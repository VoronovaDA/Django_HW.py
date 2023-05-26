from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    temperature = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')

    def __str__(self):
        return f'Sensor_{self.sensor}_{self.created_at}'
    