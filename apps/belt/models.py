from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
import datetime

Email_Regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class userManager(models.Manager):
    def validate (self, postData):
        errors = []
        today = str(datetime.date.today()).split()[0]
        print "got today", today
        if len(postData['name']) < 3:
            errors.append("Is that really your full name?")
        if len(postData['alias']) < 1:
            errors.append("Alias must be at least one character")
        if not Email_Regex.match(postData['email']):
            errors.append("Invalid email")
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors.append("Email already exists in our database")
        if postData['password'] != postData['confirm_password']:
            errors.append("Your passwords don't match")
        if len(postData['password']) < 8:
            errors.append("Password too short")
        if postData['birth_date'] > today:
            errors2.append("You can't be born in the future")
        if len(errors) == 0:
            #create the user
            newuser = User.objects.create(name= postData['name'], alias= postData['alias'], email= postData['email'], birth_date= postData['birth_date'], password= bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
            return (True, newuser)
        else:
            return (False, errors)

    def login(self, postData):
        errors1 = []
        if 'email' in postData and 'password' in postData:
            try:
                print 50*('8')
                user = User.objects.get(email = postData['email'])
            except User.DoesNotExist:
                print 50*('4')
                errors1.append("Sorry please try again")
                return (False, errors1)
        pw_match = bcrypt.hashpw(postData['password'].encode(), user.password.encode())
        print 10*"3", user.password
        if pw_match == user.password:
            return (True, user)
        else:
            errors1.append("Sorry please try again!!!!")
            return (False, errors1)

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    birth_date = models.DateTimeField()
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

class quoteManager(models.Manager):
    def quote_validate (self, postData, id):
        errors2 = []
        if len(postData['quote_by'])<3:
            errors2.append("Too short! Is that full name of the quoted")
        if len(postData['message'])<3:
            errors2.append("Too short! Quote should be at least 3 characters")
        if len(errors2) == 0:
            #create the quote
            user = User.objects.get(id=id)
            newquote = Quote.objects.create(author= user, quote_by= postData['quote_by'], message= postData['message'])
            return (True, newquote)
        else:
            return (False, errors2)

    def like(self, id, quote_id):
        errors3 = []
        if len(Quote.objects.filter(id=quote_id).filter(admirers__id=id))>0:
            errors3.append("You already favorited this quote")
            return (False, errors3)
        else:
            current_user= User.objects.get(id=id)
            quote=self.get(id=quote_id)
            admirer= quote.admirers.add(current_user)
            return (True, admirer)

class Quote(models.Model):
    author= models.ForeignKey(User, related_name="authored")
    quote_by = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)
    admirers= models.ManyToManyField(User, related_name="likes_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = quoteManager()
