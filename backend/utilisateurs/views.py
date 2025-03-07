from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import User
from django.contrib.auth import logout
import json

@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            email = data.get("email")
            pseudo = data.get("pseudo")
            nom = data.get("nom")
            prenom = data.get("prenom")
            password = data.get("password")

            print(f"Received data - Email: {email}, Pseudo: {pseudo}")

            if not email or not pseudo or not nom or not prenom or not password:
                return JsonResponse({"error": "Tous les champs sont obligatoires."}, status=400)

            user = User.objects.create_user(email=email, pseudo=pseudo, nom=nom, prenom=prenom, password=password)
            return JsonResponse({"message": "Inscription réussie !"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)

                return JsonResponse({
                    "message": "Connexion réussie !",
                    "pseudo": user.pseudo,
                    "email": user.email,
                    "nom": user.nom,
                    "prenom": user.prenom
                }, status=200)
            else:
                return JsonResponse({"error": "Email ou mot de passe incorrect"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def change_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            new_password = data.get("newPassword")

            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()

            return JsonResponse({"message": "Mot de passe changé avec succès !"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "Utilisateur non trouvé"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
def user_logout(request):
    if request.method == "POST":
        try:
            logout(request)
            return JsonResponse({"message": "Déconnexion réussie !"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)