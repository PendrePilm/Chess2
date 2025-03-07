# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, pseudo, nom, prenom, password, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire.")
        if not pseudo:
            raise ValueError("Le pseudo est obligatoire.")
        
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            pseudo=pseudo,
            nom=nom,
            prenom=prenom,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, pseudo, nom, prenom, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, pseudo, nom, prenom, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=250)
    pseudo = models.CharField(unique=True, max_length=100)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"  # Utiliser l'email comme identifiant de connexion
    REQUIRED_FIELDS = ["pseudo", "nom", "prenom"]

    def __str__(self):
        return self.pseudo