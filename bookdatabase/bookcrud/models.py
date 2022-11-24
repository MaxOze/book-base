from datetime import datetime, timedelta
from django.db import models

class BooksappBook(models.Model):
    id = models.BigAutoField(primary_key=True)
    book_name = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    price = models.IntegerField()

    class Meta:
        db_table = 'bookdb'

class BooksappRole(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=20)

    class Meta:
        db_table = 'roledb'

class BooksappUser(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.ForeignKey('booksapprole', on_delete=models.PROTECT)      # Внешний ключ для ролей

    class Meta:
        db_table = 'userdb'

class BooksappOrder(models.Model):
    id = models.AutoField(primary_key=True)
    order_date = models.DateTimeField(default=datetime.now()+timedelta(hours=5))  # По дефолту выставляет время заказа 
    order_price = models.FloatField()                                                     #(прибавляет 5 часов так как по дефолту ставит время UTC)
    order_user = models.ForeignKey('booksappuser', on_delete=models.PROTECT)

    class Meta:
        db_table = 'orderdb'

class BooksappOrderBook(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey('booksapporder', on_delete=models.PROTECT)
    book = models.ForeignKey('booksappbook', on_delete=models.PROTECT)

    class Meta:
        db_table = 'order_bookdb'