from email.mime import application
from bibliotheque import Bibliotheque, Livre,Membre
from exceptions import *
import tkinter as tk
from gui import BibliothequeApp
import os
def clearp():
    os.system('cls' if os.name == 'nt' else 'clear')
def afficherMenu():
    print("\n=== GESTION BIBLIOTHEQUE ===")
    print("1. Ajouter un livre")
    print("2. Inscrire un membre")
    print("3. Emprunter un livre")
    print("4. Rendre un livre")
    print("5. Lister tous les livres ")
    print("6. Lister tous les membres")
    print("7. Afficher les statistiques")
    print("8. Sauvgarder et quitter")
def ajouterLIVRE(bibliotheque):
    clearp()
    print("\n --Ajouter un livre--")
    isbn = input("ISBN : ")
    titre = input("Titre : ")
    auteur = input("Auteur : ")
    année = input("Annee : ")
    genre = input("Genre : ")
    try:
        année = int(année)
        livre = Livre(isbn,titre,auteur,année,genre)
        bibliotheque.ajouterLIVRE(livre)
        print(f"\nle livre '{titre}' a ete ajoute avec succes !!")
    except ValueError:
        print("Erreur: l'annee doit etre un entier")
def inscrireMEMBRE(bibliotheque):
    clearp()
    print("--Inscrire un membre--")
    ID = input("Entrez l'id du membre : ")
    nom = input("Nom Complet :")
 
    membre = Membre(ID,nom)
    bibliotheque.inscrireMEMBRE(membre)
    print(f"\n le membre '{nom}' a ete inscrit avec succes !")
    
   
    
def emprunterLIVRE(bibliotheque):
    clearp()
    print("\n --Emprunter un livre--")
    isbn = input("isbn du livre : ")
    ID = input("id du membre : ")
    try:
        bibliotheque.emprunterLIVRE(isbn, ID)
        livre = bibliotheque.trouverLIVRE(isbn)
        membre = bibliotheque.trouverMEMBRE(ID)
        print(f"\n le livre '{livre.titre}' a ete emprunte par {membre.nom}")
    except (LivreInexistantError, MembreInexistantError,LivreIndisponibleError,QuotaEmpruntDepasseError) as e: #comme dans le cours on peut traiter plusieurs exceptions a la  fois
        print(f"\n Erreur : {e}")
def rendreLIVRE(bibliotheque):
    clearp()
    print("\n --Rendre un livre--")
    isbn = input("isbn du livre : ")
    ID = input("id du membre:")
    try:
        bibliotheque.rendreLIVRE(isbn,ID)
        livre = bibliotheque.trouverLIVRE(isbn)
        membre = bibliotheque.trouverMEMBRE(ID)
        print(f"\n le livre '{livre.titre}' a ete rendu par {membre.nom}")
    except(LivreInexistantError,MembreInexistantError,Exception) as e:
        print(f"\nErreur: {e}")
def listerLIVRES(bibliotheque):
    clearp()
    print("\n--Liste de tous les livres--")
    livres = bibliotheque.listerLIVRES()
    if not livres:
        print("Il n'ya aucun livre dans notre bibliotheque")
        input("\n Appuyer sur entree pour continuer")
        return
    else:
        for i , livre in enumerate(livres,1):
            print(f"{i}.{livre}")
    #pour le choix de suppression
    print("\nOptions:")
    print("0. Retour au menu")
    print("S.Supprimer un livre")
    choix = input("\nVotre choix (0 ou S) : ").upper()
    if choix == 'S':
        try:
            num = int(input("Numero du livre a supprimer :"))
        
            num = int(num)
            if 1 <= num <= len(livres):
                livre = livres[num-1]
                if bibliotheque.supprimerLIVRE(livre.isbn):
                    print(f"\nle livre '{livre.titre}' a etet supprime avec succes ! ")
                else:
                    print("\nErreur lors de la suppression")
            else:
                print("\nnumero invalide")
        
        except ValueError:
            print("\nVeuillez entrer un nombre valide")
        input("\nAppuyer sur entree pour continuer")
    
            
def listerMEMBRES(bibliotheque):
    clearp()
    print("\n --Liste de tous les membres--")
    membres = bibliotheque.listerMEMBRES()
    if not membres:
        print("Il n'ya aucun membre inscrit")
    else:
        for membre in membres:
            print(membre)
from visualisations import afficherSTATISTIQUES
def main():
    bibliotheque = Bibliotheque()
    while True:
        afficherMenu()
        choix = input("\n Entrez votre choix :")
        try:
            
            if choix == "1":
                ajouterLIVRE(bibliotheque)
            elif choix == "2":
               inscrireMEMBRE(bibliotheque)
            elif choix == "3":
                emprunterLIVRE(bibliotheque)
            elif choix == "4":
                rendreLIVRE(bibliotheque)
            elif choix == "5":
                listerLIVRES(bibliotheque)
            elif choix == "6":
                listerMEMBRES(bibliotheque)
            elif choix == "7":
                afficherSTATISTIQUES(bibliotheque)
            elif choix == "8":
                
                bibliotheque.sauvgarderLIVRES()
                bibliotheque.sauvgarderMEMBRES()
                print("Vos donnes sont sauvgarder avec succes !")
                break
            else:
                print("\n Votre choix est invalid. Veuillez enterer un nombre entre 1 et 8")
        except Exception as e:
            print(f"\nUne erreur s'est produit :{e}")
        input("\nAppuyer sur entree pour continuer")
if __name__ == "__main__":
    print("Choisissez le mode d'interface :")
    print("1.Interface en ligne de commande ")
    print("2.Interface graphique")
    while True:
        mode = input("Votre choix (1 ou 2): ")
        if mode == "1":
            main()
            break
        elif mode == "2":
            root = tk.Tk()
            app = BibliothequeApp(root)
            root.mainloop()
            break
        else:
            print("Choix invalide !")
  
    
    
            
         