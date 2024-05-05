from django.db import models

class TrainingInfo(models.Model):
    id = models.AutoField(primary_key=True)
    epoch = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.IntegerField(help_text='累计用时，单位秒')
    user_id = models.IntegerField()
    model = models.CharField(max_length=255)
    top1_accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    top2_accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    top3_accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    top4_accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    top5_accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    top6_accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    top7_accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    top8_accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    top9_accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    top10_accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    optional_feature = models.CharField(max_length=255, null=True, blank=True)
    learning_rate = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    dataset = models.CharField(max_length=255, default='default_dataset')
    experiment_num = models.IntegerField(default=0)# 新增的experiment_num列

    class Meta:
        db_table = 'training_info'

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    class Meta:
        db_table = 'users'