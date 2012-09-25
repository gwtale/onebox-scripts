from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    def __unicode__(self):
        return '%s %s' %(self.first_name, self.last_name)

class Publisher(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return '%s' %(self.name)

class Genre(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return '%s' %(self.name)

class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.FloatField(db_column='rating')
    rating_count = models.IntegerField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, null=True, blank=True, 
                                  on_delete=models.SET_NULL)
    related = models.ManyToManyField('self', db_column='related', blank=True)
    genre = models.ForeignKey(Genre, null=True, blank=True, 
                              on_delete=models.SET_NULL)
    def __unicode__(self):
        return '%s' %(self.title)

class City(models.Model):
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    def __unicode__(self):
        return '%s, %s' %(self.city, self.state)

class BookStore(models.Model):
    name =  models.CharField(max_length=50)
    city = models.ForeignKey('City')
    def __unicode__(self):
        return '%s' %(self.name)
    
class SalesHistory(models.Model):
    bookstore = models.ForeignKey(BookStore)
    book = models.ForeignKey(Book)
    sale_date = models.DateField()
    sale_qty = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    def __unicode__(self):
        return '%s %s %s' %(self.bookstore, self.book, self.sale_date)
