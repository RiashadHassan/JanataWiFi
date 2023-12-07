from django.db import models

class SQLMODEL(models.Model):
    date_column = models.DateField(null=True, blank= True)
    trade_code_column = models.CharField(max_length=100, null=True, blank=True)
    high_column = models.DecimalField(decimal_places=1, max_digits=200)
    low_column = models.DecimalField(decimal_places=1, max_digits=200)
    open_column = models.DecimalField(decimal_places=1, max_digits=200)
    close_column =models.DecimalField(decimal_places=1, max_digits=200)
    volume_column = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.trade_code_column
    
    class Meta:
        ordering= ['-date_column']