import matplotlib.pyplot as plt
from bibliotheque import Bibliotheque
def afficherSTATISTIQUES(bibliotheque):
    print("--les statistiques--")
    print(f"Nombre total de livres:{len(bibliotheque.livres)}")
    print(f"Nombre total de membres:{len(bibliotheque.membres)}")
    livresDisp = sum(1 for livre in bibliotheque.livres if livre.statut == "disponible")
    print(f"livres disponibles: {livresDisp}")
    print(f"Livres emprunts:{len(bibliotheque.livres) - livresDisp}")
    #par genre
    genres = {}
    for livre in bibliotheque.livres:
        genres[livre.genre] = genres.get(livre.genre, 0) + 1
    print("repartition par genre:")
    for genre, count in genres.items():
        print(f"-{genre}: {count} livre(s)")
    #cerculaire
    if genres:
        plt.figure(figsize=(8, 6))
        plt.pie(genres.values(), labels=genres.keys(), autopct='%1.1f%%')
        plt.title('repatition de livres par genre')
        plt.savefig('assets/stats_genres.png')# hadi oN la fAIT POUR QUE LE DIAGRAMME SOIT SAUVEGARDEE AUTOMATIQUEMT DANS stats_genres.png
        plt.show()
    #histogramme
    auteurs = {}
    for livre in bibliotheque.livres:
        auteurs[livre.auteur] = auteurs.get(livre.auteur, 0) + 1
    if auteurs:
        auteurs10 = sorted(auteurs.items(), key=lambda x: x[1], reverse=True)[:10]
        nomauteurs = [a[0] for a in auteurs10]
        nblivres = [a[1] for a in auteurs10]
        plt.figure(figsize=(10, 6))
        plt.bar(nomauteurs, nblivres)
        plt.xlabel('Auteurs')
        plt.ylabel('Nombres de livres ')
        plt.title('Top 10')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig('assets/stats_auteurs.png')
        plt.show()
    #Courbe
    try:
        with open('data/historique.csv' , 'r') as f:
            dates = []
            for line in f:
                date, _, _, action = line.strip().split(';')
                if action == 'emprunt':
                    dates.append(date)
        if dates:
            from collections import defaultdict
            from datetime import datetime, timedelta 
            empruntspardate = defaultdict(int)
            for date in dates:
                empruntspardate[date] += 1
                datefin = datetime.now()
                datedebut = datefin - timedelta(days=30)
                jours = [(datefin - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)][::-1]
                valeurs = [empruntspardate.get(jour, 0) for jour in jours]
                plt.figure(figsize=(12, 6))
                plt.plot(jours, valeurs, marker='o')
                plt.xlabel('Date')
                plt.ylabel('NOmbre demprunts')
                plt.title('Activite demprunts 30 jours')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
    except FileNotFoundError:
        print("\naucun historique demprunts")
    