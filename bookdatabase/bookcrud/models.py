from django.db import models

class BooksappBook(models.Model):
    id = models.BigAutoField(primary_key=True)
    book_name = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    price = models.IntegerField()

    class Meta:
        db_table = 'bookdb'