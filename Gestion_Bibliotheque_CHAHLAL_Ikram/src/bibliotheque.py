import json
from datetime import datetime
from exceptions import *
class Livre:
    def __init__(self,isbn,titre,auteur,année,genre,statut ="disponible"):
        self.isbn = isbn
        self.titre = titre
        self.auteur = auteur
        self.année = année
        self.genre = genre
        self.statut = statut
    def __str__(self):
        return f" livre :{self.titre} son isbn : {self.isbn} de :{self.auteur} son genre:{self.genre} publie en :{self.année}"

class Membre:
    def __init__(self,ID,nom):
        self.ID = ID
        self.nom = nom
        self.livres_empruntes = []
    def __str__(self):
        return f"ID : {self.ID} nom :{self.nom}-  Livres empruntes:{len(self.livres_empruntes)}"    
class Bibliotheque:
    def __init__(self):
        self.livres = []
        self.membres = []
        self.chargerDONNEES()
        
    def ajouterLIVRE(self,livre):
        self.livres.append(livre)
        self.sauvgarderLIVRES()
        
    def supprimerLIVRE(self,isbn):
        livre = self.trouverLIVRE(isbn)
        if livre:   #cad on trouve le livre
            self.livres.remove(livre)
            self.sauvgarderLIVRES()
            return True
        return False
    
    def inscrireMEMBRE(self,membre):
        self.membres.append(membre)
        self.sauvgarderMEMBRES()
    def emprunterLIVRE(self,isbn,ID):
        livre = self.trouverLIVRE(isbn)
        membre = self.trouverMEMBRE(ID)
        
        if not livre :
            raise LivreInexistantError(f"Le livre avec le isbn {isbn} n'existe pas !")
        if not membre :
            raise MembreInexistantError(f"Le livre avec l'ID {ID} n'existe pas !")
        if livre.statut != "disponible":
            raise LivreIndisponibleError(f"Le livre {livre.titre} n'est pas disponible !")
        if len(membre.livres_empruntes) >= 3 :
            raise QuotaEmpruntDepasseError(f"Le membre {membre.nom} a atteint son quota d'emprunt !")
        livre.statut = "emprunté"
        membre.livres_empruntes.append(isbn)
        self.enregistrerHISTORIQUE(isbn,ID,"emprunt")
        self.sauvgarderLIVRES()
        self.sauvgarderMEMBRES()
    def rendreLIVRE(self,isbn,ID):
        livre = self.trouverLIVRE(isbn)
        membre = self.trouverMEMBRE(ID)
        if not livre :
            raise LivreInexistantError(f"Le livre avec le isbn :{isbn} n'exixte pas")
        if not membre :
            raise MembreInexistantError(f"Le membre avec le ID : {ID} n'existe pas")
        if isbn not in membre.livres_empruntes:
            raise Exception(f"le membre : {membre.nom} n'a pas emprunter ce livre")
        livre.statut = "disponible"
        membre.livres_empruntes.remove(isbn)
        self.enregistrerHISTORIQUE(isbn,ID,  "retour")
        self.sauvgarderLIVRES()
        self.sauvgarderMEMBRES()
    def trouverLIVRE(self, isbn):
        for livre in self.livres:
            if livre.isbn == isbn:
                return livre
        return None
    def trouverMEMBRE(self,ID):
        for membre in self.membres:
            if membre.ID == ID:
                return membre
        return None
    def listerLIVRES(self):
        return self.livres
    def listerMEMBRES(self):
        return self.membres
    def enregistrerHISTORIQUE(self,isbn,ID,action):
        with open("data/historique.csv" , "a") as f :
            f.write(f"{datetime.now().strftime('%Y-%m-%d')};{isbn};{ID};{action}\n")
    def sauvgarderLIVRES(self):
        with open("data/livres.txt" , "w") as f:
            for livre in self.livres:
                f.write(f"{livre.isbn};{livre.titre};{livre.auteur};{livre.année};{livre.genre};{livre.statut}\n")
    def sauvgarderMEMBRES(self):
        with open("data/membres.txt" , "w") as f:
            for membre in self.membres:
                livres_str = ",".join(membre.livres_empruntes)
                f.write(f"{membre.ID};{membre.nom};{livres_str}\n")
    def chargerDONNEES(self):
        try:
            with open("data/livres.txt", "r") as f:
                for line in f:
                    isbn,titre,auteur,année,genre,statut = line.strip().split(";")
                    self.livres.append(Livre(isbn,titre,auteur,int(année),genre,statut))
        except FileNotFoundError:
            pass
        try:
            with open("data/membres.txt", "r") as f:
                for line in f:
                    parts = line.strip().split(";")
                    ID,nom = parts[0],parts[1]
                    livres_empruntes = parts[2].split(",") if len(parts) > 2 and parts[2] else []
                    membre = Membre(ID,nom)
                    membre.livres_empruntes = livres_empruntes
                    self.membres.append(membre)
        except FileNotFoundError:
            pass