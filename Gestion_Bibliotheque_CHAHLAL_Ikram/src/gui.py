import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font
from bibliotheque import Bibliotheque, Livre, Membre
from exceptions import *
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from PIL import Image, ImageTk

class BibliothequeApp:
    def __init__(self, root):
        self.root = root
        self.bibliotheque = Bibliotheque()
        self.setup_ui()
        self.create_menu()
        self.setup_notebook()
        self.load_data()
        
    def setup_ui(self):
        self.root.title("Système de Gestion de Bibliothèque")
        self.root.geometry("600x700")
        self.root.minsize(1000, 600)
        self.root.configure(bg='#FFF0F5')  
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        bg_color = '#FFF0F5'  
        header_color = '#E6E6FA'  
        button_color = '#D8BFD8'  
        active_button_color = '#DDA0DD' 
        text_color = '#4B0082'  
        frame_color = '#F8F8FF'  
        self.style.configure('.', background=bg_color, foreground=text_color)
        self.style.configure('TFrame', background=bg_color)
        self.style.configure('TLabel', background=bg_color, foreground=text_color, font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10), padding=5, 
                            background=button_color, foreground=text_color)
        self.style.map('TButton', 
                      background=[('active', active_button_color), ('pressed', '#9370DB')],
                      foreground=[('active', text_color)])
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'), foreground='#800080')  # Violet
        self.style.configure('Treeview', font=('Helvetica', 10), background='white', fieldbackground='white')
        self.style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'), background=header_color)
        self.style.configure('TNotebook', background=bg_color)
        self.style.configure('TNotebook.Tab', background=button_color, padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', header_color)])
        self.style.configure('TLabelframe', background=bg_color, foreground=text_color)
        self.style.configure('TLabelframe.Label', background=bg_color, foreground='#800080')
        self.style.configure('TEntry', fieldbackground='white')
        
        header_frame = ttk.Frame(self.root, style='TFrame')
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_font = Font(family='Helvetica', size=18, weight='bold')
        ttk.Label(header_frame, text="SYSTÈME DE GESTION DE BIBLIOTHÈQUE", 
                 font=title_font, foreground='#800080', background=header_color).pack(side=tk.LEFT, padx=10, pady=5, ipadx=10, ipady=5)
        
        self.status_var = tk.StringVar()
        self.status_var.set("")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                                   relief=tk.SUNKEN, anchor=tk.W, 
                                   background=header_color, foreground=text_color)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_menu(self):
        menubar = tk.Menu(self.root, bg='#E6E6FA', fg='#4B0082', activebackground='#DDA0DD', activeforeground='#4B0082')
        
        file_menu = tk.Menu(menubar, tearoff=0, bg='#FFF0F5', fg='#4B0082', activebackground='#DDA0DD', activeforeground='#4B0082')
        file_menu.add_command(label="Sauvegarder", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        
        help_menu = tk.Menu(menubar, tearoff=0, bg='#FFF0F5', fg='#4B0082', activebackground='#DDA0DD', activeforeground='#4B0082')
        help_menu.add_command(label="À propos", command=self.show_about)
        menubar.add_cascade(label="Aide", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def setup_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.livres_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.livres_frame, text="Livres")
        self.setup_livres_tab()
        
        self.membres_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.membres_frame, text="Membres")
        self.setup_membres_tab()
        
        self.emprunts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.emprunts_frame, text="Emprunts")
        self.setup_emprunts_tab()
        
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Statistiques")
        self.setup_stats_tab()
    
    def setup_livres_tab(self):
        left_frame = ttk.Frame(self.livres_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        form_frame = ttk.LabelFrame(left_frame, text="Ajouter/Modifier un Livre", style='TLabelframe')
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="ISBN:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.isbn_entry = ttk.Entry(form_frame)
        self.isbn_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Titre:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.titre_entry = ttk.Entry(form_frame)
        self.titre_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Auteur:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.auteur_entry = ttk.Entry(form_frame)
        self.auteur_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Année:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.annee_entry = ttk.Entry(form_frame)
        self.annee_entry.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Genre:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.genre_entry = ttk.Entry(form_frame)
        self.genre_entry.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)
        
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Ajouter", command=self.add_livre).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Effacer", command=self.clear_livre_form).pack(side=tk.LEFT, padx=5)
        
        right_frame = ttk.Frame(self.livres_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        list_frame = ttk.LabelFrame(right_frame, text="Liste des Livres", style='TLabelframe')
        list_frame.pack(fill=tk.BOTH, expand=True)
        self.root.geometry("300x300")
        
        columns = ("isbn", "titre", "auteur", "année", "genre", "statut")
        self.livres_tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        
        for col in columns:
            self.livres_tree.heading(col, text=col.capitalize())
            self.livres_tree.column(col, width=100, anchor=tk.W)
        
        self.livres_tree.column("titre", width=200)
        self.livres_tree.column("auteur", width=150)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.livres_tree.yview)
        self.livres_tree.configure(yscrollcommand=scrollbar.set)
        
        self.livres_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.livres_tree.bind("<<TreeviewSelect>>", self.on_livre_select)
        
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(search_frame, text="Rechercher:").pack(side=tk.LEFT, padx=5)
        self.livre_search_entry = ttk.Entry(search_frame)
        self.livre_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.livre_search_entry.bind("<KeyRelease>", self.search_livres)
        
    
    def setup_membres_tab(self):
        left_frame = ttk.Frame(self.membres_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        form_frame = ttk.LabelFrame(left_frame, text="Ajouter/Modifier un Membre", style='TLabelframe')
        form_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.membre_id_entry = ttk.Entry(form_frame)
        self.membre_id_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Nom:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.membre_nom_entry = ttk.Entry(form_frame)
        self.membre_nom_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Ajouter", command=self.add_membre).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Effacer", command=self.clear_membre_form).pack(side=tk.LEFT, padx=5)
        
        right_frame = ttk.Frame(self.membres_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        list_frame = ttk.LabelFrame(right_frame, text="Liste des Membres", style='TLabelframe')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("id", "nom", "livres_empruntes")
        self.membres_tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        
        self.membres_tree.heading("id", text="ID")
        self.membres_tree.heading("nom", text="Nom")
        self.membres_tree.heading("livres_empruntes", text="Livres Empruntés")
        
        self.membres_tree.column("id", width=100, anchor=tk.W)
        self.membres_tree.column("nom", width=200, anchor=tk.W)
        self.membres_tree.column("livres_empruntes", width=300, anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.membres_tree.yview)
        self.membres_tree.configure(yscrollcommand=scrollbar.set)
        
        self.membres_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.membres_tree.bind("<<TreeviewSelect>>", self.on_membre_select)
        
        search_frame = ttk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(search_frame, text="Rechercher:").pack(side=tk.LEFT, padx=5)
        self.membre_search_entry = ttk.Entry(search_frame)
        self.membre_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.membre_search_entry.bind("<KeyRelease>", self.search_membres)
        
    
    def setup_emprunts_tab(self):
        top_frame = ttk.Frame(self.emprunts_frame)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        emprunt_frame = ttk.LabelFrame(top_frame, text="Emprunter un Livre", style='TLabelframe')
        emprunt_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Label(emprunt_frame, text="ISBN du Livre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.emprunt_isbn_entry = ttk.Entry(emprunt_frame)
        self.emprunt_isbn_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(emprunt_frame, text="ID du Membre:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.emprunt_membre_entry = ttk.Entry(emprunt_frame)
        self.emprunt_membre_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Button(emprunt_frame, text="Emprunter", command=self.emprunter_livre).grid(row=2, column=0, columnspan=2, pady=5)
        
        retour_frame = ttk.LabelFrame(top_frame, text="Retourner un Livre", style='TLabelframe')
        retour_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Label(retour_frame, text="ISBN du Livre:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.retour_isbn_entry = ttk.Entry(retour_frame)
        self.retour_isbn_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(retour_frame, text="ID du Membre:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.retour_membre_entry = ttk.Entry(retour_frame)
        self.retour_membre_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Button(retour_frame, text="Retourner", command=self.retourner_livre).grid(row=2, column=0, columnspan=2, pady=5)
        
        bottom_frame = ttk.Frame(self.emprunts_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        history_frame = ttk.LabelFrame(bottom_frame, text="Historique des Emprunts", style='TLabelframe')
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("date", "isbn", "id_membre", "action")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        
        for col in columns:
            self.history_tree.heading(col, text=col.capitalize())
            self.history_tree.column(col, width=100, anchor=tk.W)
        
        self.history_tree.column("date", width=150)
        
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_stats_tab(self):
        stats_frame = ttk.Frame(self.stats_frame)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        button_frame = ttk.Frame(stats_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(button_frame, text="Afficher Statistiques", command=self.show_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exporter Graphiques", command=self.export_graphs).pack(side=tk.LEFT, padx=5)
        
        self.figure_frame = ttk.Frame(stats_frame)
        self.figure_frame.pack(fill=tk.BOTH, expand=True)
        
        info_frame = ttk.Frame(stats_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.stats_var = tk.StringVar()
        ttk.Label(info_frame, textvariable=self.stats_var, wraplength=800).pack()
        
        self.update_stats_info()
    
    def load_data(self):
        self.update_livres_list()
        self.update_membres_list()
        self.update_history_list()
        self.update_stats_info()
    
    def save_data(self):
        self.bibliotheque.sauvgarderLIVRES()
        self.bibliotheque.sauvgarderMEMBRES()
        self.status_var.set("Données sauvegardées avec succès")
    
    def update_livres_list(self):
        self.livres_tree.delete(*self.livres_tree.get_children())
        for livre in self.bibliotheque.listerLIVRES():
            self.livres_tree.insert("", tk.END, 
                                  values=(livre.isbn, livre.titre, livre.auteur, 
                                          livre.année, livre.genre, livre.statut))
    
    def update_membres_list(self):
        self.membres_tree.delete(*self.membres_tree.get_children())
        for membre in self.bibliotheque.listerMEMBRES():
            livres_str = ", ".join(membre.livres_empruntes) if membre.livres_empruntes else "Aucun"
            self.membres_tree.insert("", tk.END, 
                                   values=(membre.ID, membre.nom, livres_str))
    
    def update_history_list(self):
        self.history_tree.delete(*self.history_tree.get_children())
        try:
            with open('data/historique.csv', 'r') as f:
                for line in f:
                    date, isbn, id_membre, action = line.strip().split(';')
                    self.history_tree.insert("", tk.END, values=(date, isbn, id_membre, action))
        except FileNotFoundError:
            pass
    
    def update_stats_info(self):
        total_livres = len(self.bibliotheque.livres)
        total_membres = len(self.bibliotheque.membres)
        livres_dispo = sum(1 for livre in self.bibliotheque.livres if livre.statut == "disponible")
        
        stats_text = (f"Statistiques de la bibliothèque:\n"
                     f"• Nombre total de livres: {total_livres}\n"
                     f"• Nombre total de membres: {total_membres}\n"
                     f"• Livres disponibles: {livres_dispo}\n"
                     f"• Livres empruntés: {total_livres - livres_dispo}")
        
        self.stats_var.set(stats_text)
    
    def add_livre(self):
        isbn = self.isbn_entry.get()
        titre = self.titre_entry.get()
        auteur = self.auteur_entry.get()
        annee = self.annee_entry.get()
        genre = self.genre_entry.get()
        
        if not all([isbn, titre, auteur, annee, genre]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires")
            return
        
        try:
            annee = int(annee)
            livre = Livre(isbn, titre, auteur, annee, genre)
            self.bibliotheque.ajouterLIVRE(livre)
            self.update_livres_list()
            self.clear_livre_form()
            self.status_var.set(f"Livre '{titre}' ajouté avec succès")
        except ValueError:
            messagebox.showerror("Erreur", "L'année doit être un nombre entier")
    
    
    def clear_livre_form(self):
        self.isbn_entry.delete(0, tk.END)
        self.titre_entry.delete(0, tk.END)
        self.auteur_entry.delete(0, tk.END)
        self.annee_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
    
    def on_livre_select(self, event):
        selected = self.livres_tree.selection()
        if not selected:
            return
        
        item = self.livres_tree.item(selected[0])
        values = item['values']
        
        self.clear_livre_form()
        
        self.isbn_entry.insert(0, values[0])
        self.titre_entry.insert(0, values[1])
        self.auteur_entry.insert(0, values[2])
        self.annee_entry.insert(0, values[3])
        self.genre_entry.insert(0, values[4])
    
    def search_livres(self, event=None):
        query = self.livre_search_entry.get().lower()
        
        self.livres_tree.delete(*self.livres_tree.get_children())
        
        for livre in self.bibliotheque.listerLIVRES():
            if (query in livre.isbn.lower() or 
                query in livre.titre.lower() or 
                query in livre.auteur.lower() or 
                query in livre.genre.lower()):
                self.livres_tree.insert("", tk.END, 
                                      values=(livre.isbn, livre.titre, livre.auteur, 
                                              livre.année, livre.genre, livre.statut))
    
    def add_membre(self):
        id_membre = self.membre_id_entry.get()
        nom = self.membre_nom_entry.get()
        
        if not all([id_membre, nom]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires")
            return
        
        membre = Membre(id_membre, nom)
        self.bibliotheque.inscrireMEMBRE(membre)
        self.update_membres_list()
        self.clear_membre_form()
        self.status_var.set(f"Membre '{nom}' ajouté avec succès")
    
    
    def clear_membre_form(self):
        self.membre_id_entry.delete(0, tk.END)
        self.membre_nom_entry.delete(0, tk.END)
    
    def on_membre_select(self, event):
        selected = self.membres_tree.selection()
        if not selected:
            return
        
        item = self.membres_tree.item(selected[0])
        values = item['values']
        
        self.clear_membre_form()
        
        self.membre_id_entry.insert(0, values[0])
        self.membre_nom_entry.insert(0, values[1])
    
    def search_membres(self, event=None):
        query = self.membre_search_entry.get().lower()
        
        self.membres_tree.delete(*self.membres_tree.get_children())
        
        for membre in self.bibliotheque.listerMEMBRES():
            if (query in membre.ID.lower() or 
                query in membre.nom.lower()):
                livres_str = ", ".join(membre.livres_empruntes) if membre.livres_empruntes else "Aucun"
                self.membres_tree.insert("", tk.END, 
                                       values=(membre.ID, membre.nom, livres_str))
    
    def emprunter_livre(self):
        isbn = self.emprunt_isbn_entry.get()
        id_membre = self.emprunt_membre_entry.get()
        
        if not all([isbn, id_membre]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires")
            return
        
        try:
            self.bibliotheque.emprunterLIVRE(isbn, id_membre)
            livre = self.bibliotheque.trouverLIVRE(isbn)
            membre = self.bibliotheque.trouverMEMBRE(id_membre)
            
            self.update_livres_list()
            self.update_membres_list()
            self.update_history_list()
            
            self.emprunt_isbn_entry.delete(0, tk.END)
            self.emprunt_membre_entry.delete(0, tk.END)
            
            self.status_var.set(f"Livre '{livre.titre}' emprunté par {membre.nom}")
        except (LivreInexistantError, MembreInexistantError, 
                LivreIndisponibleError, QuotaEmpruntDepasseError) as e:
            messagebox.showerror("Erreur", str(e))
    
    def retourner_livre(self):
        isbn = self.retour_isbn_entry.get()
        id_membre = self.retour_membre_entry.get()
        
        if not all([isbn, id_membre]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires")
            return
        
        try:
            self.bibliotheque.rendreLIVRE(isbn, id_membre)
            livre = self.bibliotheque.trouverLIVRE(isbn)
            membre = self.bibliotheque.trouverMEMBRE(id_membre)
            
            self.update_livres_list()
            self.update_membres_list()
            self.update_history_list()
            
            self.retour_isbn_entry.delete(0, tk.END)
            self.retour_membre_entry.delete(0, tk.END)
            
            self.status_var.set(f"Livre '{livre.titre}' retourné par {membre.nom}")
        except (LivreInexistantError, MembreInexistantError, Exception) as e:
            messagebox.showerror("Erreur", str(e))
    
    def show_stats(self):
        for widget in self.figure_frame.winfo_children():
            widget.destroy()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.subplots_adjust(wspace=0.4)
        
        genres = {}
        for livre in self.bibliotheque.livres:
            genres[livre.genre] = genres.get(livre.genre, 0) + 1
        
        if genres:
            colors = ['#FFB6C1', '#DDA0DD', '#87CEFA', '#98FB98', '#FFD700', '#FFA07A', '#E0FFFF', '#FFC0CB', '#D8BFD8', '#B0E0E6']
            ax1.pie(genres.values(), labels=genres.keys(), autopct='%1.1f%%', colors=colors[:len(genres)])
            ax1.set_title('Répartition des livres par genre')
        
        auteurs = {}
        for livre in self.bibliotheque.livres:
            auteurs[livre.auteur] = auteurs.get(livre.auteur, 0) + 1
        
        if auteurs:
            auteurs10 = sorted(auteurs.items(), key=lambda x: x[1], reverse=True)[:10]
            noms = [a[0] for a in auteurs10]
            counts = [a[1] for a in auteurs10]
            
            ax2.bar(noms, counts, color='#DDA0DD')
            ax2.set_title('Top 10 des auteurs')
            ax2.set_ylabel('Nombre de livres')
            ax2.tick_params(axis='x', rotation=45)
        
        canvas = FigureCanvasTkAgg(fig, master=self.figure_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.update_stats_info()
    
    def export_graphs(self):
        if not os.path.exists('assets'):
            os.makedirs('assets')
        
        genres = {}
        for livre in self.bibliotheque.livres:
            genres[livre.genre] = genres.get(livre.genre, 0) + 1
        
        if genres:
            plt.figure(figsize=(8, 6))
            colors = ['#FFB6C1', '#DDA0DD', '#87CEFA', '#98FB98', '#FFD700', '#FFA07A', '#E0FFFF', '#FFC0CB', '#D8BFD8', '#B0E0E6']
            plt.pie(genres.values(), labels=genres.keys(), autopct='%1.1f%%', colors=colors[:len(genres)])
            plt.title('Répartition des livres par genre')
            plt.savefig('assets/stats_genres.png')
            plt.close()
        
        auteurs = {}
        for livre in self.bibliotheque.livres:
            auteurs[livre.auteur] = auteurs.get(livre.auteur, 0) + 1
        
        if auteurs:
            auteurs10 = sorted(auteurs.items(), key=lambda x: x[1], reverse=True)[:10]
            noms = [a[0] for a in auteurs10]
            counts = [a[1] for a in auteurs10]
            
            plt.figure(figsize=(10, 6))
            plt.bar(noms, counts, color='#DDA0DD')
            plt.xlabel('Auteurs')
            plt.ylabel('Nombre de livres')
            plt.title('Top 10 des auteurs')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig('assets/stats_auteurs.png')
            plt.close()
        
        try:
            with open('data/historique.csv', 'r') as f:
                dates = []
                for line in f:
                    date, _, _, action = line.strip().split(';')
                    if action == 'emprunt':
                        dates.append(date)
            
            if dates:
                from collections import defaultdict
                from datetime import datetime, timedelta
                
                emprunts_par_date = defaultdict(int)
                for date in dates:
                    emprunts_par_date[date] += 1
                
                date_fin = datetime.now()
                date_debut = date_fin - timedelta(days=30)
                jours = [(date_fin - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)][::-1]
                valeurs = [emprunts_par_date.get(jour, 0) for jour in jours]
                
                plt.figure(figsize=(12, 6))
                plt.plot(jours, valeurs, marker='o', color='#9370DB')
                plt.xlabel('Date')
                plt.ylabel('Nombre d\'emprunts')
                plt.title('Activité des emprunts (30 derniers jours)')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig('assets/stats_activite.png')
                plt.close()
        except FileNotFoundError:
            pass
        
        self.status_var.set("Graphiques exportés dans le dossier 'assets'")
    
    def show_about(self):
        about_text = ("Système de Gestion de Bibliothèque\n"
                     )
        messagebox.showinfo("À propos", about_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = BibliothequeApp(root)
    root.mainloop()