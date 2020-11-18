from django.db import models
import re
from datetime import date, datetime
from time import strptime
EMAIL_REGEX = re.compile('^[_a-z0-9-]+(.[_a-z0-9-]+)@[a-z0-9-]+(.[a-z0-9-]+)(.[a-z]{2,4})$')



class UserManager(models.Manager):

    def basic_validator(self, postData):
        
        errors = []
        print(postData)
        if len(postData['first_name']) < 2 or len(postData['first_name']) == 0:
            errors.append('First Name required; must be at least 2 characters')
        # if len(postData['first_name']) == 0:
            # errors.append('First Name required!')
        if len(postData['last_name']) < 2 or len(postData['last_name']) == 0:
            errors.append('Last Name required; must be at least 2 characters')
        
        # if len(postData['last_name']) < 2:
        #     errors.append('Last Name must be at least 2 characters')
        
        if len(postData['password'])< 8 or len(postData['cpassword'])< 8:
            errors.append('Password and password confirmation must be at least 8 digits')
        
        # if len(postData['cpassword'])< 8:
        #     errors.append('Password confirmation must be at least 8 digits')

        if postData['password'] != postData['cpassword']:
            errors.append('Password and password confirm does not match!')

        if not re.match(EMAIL_REGEX, postData['email']):
            errors.append('Email is not valid!') 
        
        for user in User.objects.filter(email = postData['email']):
            if user:
                errors.append('The email address already exists! please choose another one') 
        
        if not (postData['first_name'].isalpha() and postData['last_name'].isalpha()):
            errors.append('First name and Last name can only contain alphabet letters!')
        

        return errors

    def validator(self, postData):
        errors = []
        # for user in User.objects.filter(email = postData['email']):
        #     if not user:
        errors.append('Email does not exist!')


        return errors
class TravelManager(models.Manager):

    def validator(self, postData):
        errors = []
        
        if not postData['description']:
            errors.append('A Plan field must be provided!')
        
        if not postData['start']:
            errors.append('A Start Date field must be provided!')
        
        if not postData['end']:
            errors.append('An End Date field must be provided!')
    
        if len(postData['description']) <3:
            errors.append('A Plan must consist of at least 3 characters!')

        if not postData['destination']: 
            errors.append( "A description field must be provided! must consist of at least 3 characters!")
        
        if len(postData['destination']) <3:
            errors.append('A destination must consist of at least 3 characters!')
        
        if str(date.today()) > str(postData['start']):
            errors.append(" Start Date can not be in the past")
        if str(date.today()) > postData['end']:
            errors.append(" End date must be in the future")
        if postData['start'] > postData['end']:
            errors.append("time travel is not allowed")
        return errors
    def join(self, user_id, travel_id):
        if len(Travel.objects.filter(id=travel_id).filter(join__id=user_id))>0:
            return {'errors':' already Joined '}
        else:
            joiner= User.objects.get(id=user_id)
            plan= self.get(id= travel_id)
            plan.join.add(joiner)
            return {}

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= UserManager()

class Travel(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start= models.DateField()
    end= models.DateField()
    creator= models.ForeignKey(User, related_name= "planner", on_delete=models.CASCADE)
    join= models.ManyToManyField(User, related_name="joiner") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= TravelManager()
