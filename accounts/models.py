from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager




class AdminUserManager(BaseUserManager):

    def create_user(self, name, surname, email, flat, phone_number, password=None):

        if not email:
            raise ValueError('This user has to have an email')


        user = self.model(
            email = self.normalize_email(email),
            name = name,
            surname = surname,
            flat = flat,
            phone_number = phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user



    def create_admin(self, name, email, password=None):

        if not email:
            raise ValueError('This user has to have an email')

        user = self.model(
            email = self.normalize_email(email),
            name = 'Admin',
        )

        user.set_password(password)
        
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        

        user.save(using=self._db)
        return user



    def create_superuser(self, email, name, password):

        user = self.model(
            email = self.normalize_email(email),
            password = password,
            name = name,
        )

        user.set_password(password)

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using= self._db)
        return user




class PortalUser(AbstractBaseUser):

    name        = models.CharField(max_length=15, null=True, blank=False)
    surname     = models.CharField(max_length=30, null=True, blank=True)
    email       = models.EmailField(max_length=50, null=True, blank=False, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True, unique=True)
    flat        = models.CharField(max_length=4, null=True, blank=True)
   
   

    #required
    date_joined  = models.DateTimeField(auto_now_add=True)
    last_login   = models.DateTimeField(auto_now_add=True)
    is_admin     = models.BooleanField(default=False)
    is_staff     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=False)
    is_superadmin= models.BooleanField(default=False)

    objects = AdminUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

