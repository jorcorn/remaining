from django.db import models


class input_data(models.Model):

    oxide_method = models.CharField(max_length=20, default='equation')
    stress_curve = models.CharField(max_length=20, default='Average')
    material = models.CharField(max_length=50,
                                default='T22 2.25Cr-1Mo'
                                )

    pressure = models.FloatField()
    od = models.FloatField()
    min_wall_thickness = models.FloatField()
    tube_age = models.FloatField()
    measured_oxide_thickness = models.FloatField()
    thickest_wall = models.FloatField()
    thinnest_wall = models.FloatField()
    oxide_growth_rate = models.FloatField(null=True)
    est_op_temp = models.FloatField(null=True)
    key = models.FloatField(null=True)