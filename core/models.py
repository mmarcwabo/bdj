from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
import uuid


class BaseModel(models.Model):
    """Modèle de base avec champs communs"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    est_actif = models.BooleanField(default=True)
    
    class Meta:
        abstract = True


class Tribunal(BaseModel):
    """Informations sur les tribunaux/juridictions"""
    TYPES_TRIBUNAL = [
        ('COUR_CASSATION', 'Cour de Cassation'),
        ('COUR_APPEL', 'Cour d\'Appel'),
        ('TGI', 'Tribunal de Grande Instance'),
        ('TRIBUNAL_DU_TRAVAIL', 'Tribunal du Travail'),
        ('TRIBUNAL_COMMERCE', 'Tribunal de Commerce'),
        ('TRIPAIX', 'Tribunal de Paix'),
        ('TPE', 'Tribunal pour Enfants'),
    ]
    
    nom = models.CharField(max_length=200)
    type_tribunal = models.CharField(max_length=30, choices=TYPES_TRIBUNAL)
    juridiction = models.CharField(max_length=100)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    def __str__(self):
        return f"{self.nom} - {self.juridiction}"
    
    class Meta:
        verbose_name = "Tribunal"
        verbose_name_plural = "Tribunaux"


class Parquet(BaseModel):
    """Parquets et ministère public"""
    TYPES_PARQUET = [
        ('PARQUET_GENERAL', 'Parquet Général'),
        ('PGI', 'Parquet de Grande Instance'),
        ('PPTP', 'Parquet Près le Tribunal de Paix'),
    ]
    
    nom = models.CharField(max_length=200)
    type_parquet = models.CharField(max_length=25, choices=TYPES_PARQUET)
    tribunal = models.ForeignKey(Tribunal, on_delete=models.CASCADE, related_name='parquets')
    adresse = models.TextField()
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    competence_territoriale = models.TextField(help_text="Ressort territorial")
    competence_materielle = models.TextField(help_text="Compétences spécialisées", blank=True)
    
    def __str__(self):
        return f"{self.nom} - {self.tribunal.nom}"
    
    class Meta:
        verbose_name = "Parquet"
        verbose_name_plural = "Parquets"


class Magistrat(BaseModel):
    """Informations sur les magistrats"""
    TYPES_MAGISTRAT = [
        ('SIEGE', 'Magistrat du Siège'),
        ('PARQUET', 'Magistrat du Parquet'),
        ('DETACHE', 'Magistrat Détaché'),
    ]
    
    GRADES_SIEGE = [
        ('PRESIDENT_TJ', 'Président de Tribunal Judiciaire'),
        ('VICE_PRESIDENT', 'Vice-Président'),
        ('PRESIDENT_CHAMBRE', 'Président de Chambre'),
        ('JUGE', 'Juge'),
        ('JUGE_INSTRUCTION', 'Juge d\'Instruction'),
        ('JUGE_ENFANTS', 'Juge des Enfants'),
        ('JUGE_APPLICATION_PEINES', 'Juge de l\'Application des Peines'),
    ]
    
    GRADES_PARQUET = [
        ('PROCUREUR_GENERAL', 'Procureur Général'),
        ('AVOCAT_GENERAL', 'Avocat Général'),
        ('PROCUREUR_REPUBLIQUE', 'Procureur de la République'),
        ('VICE_PROCUREUR', 'Vice-Procureur'),
        ('SUBSTITUT', 'Substitut du Procureur'),
    ]
    
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_employe = models.CharField(max_length=50, unique=True)
    type_magistrat = models.CharField(max_length=10, choices=TYPES_MAGISTRAT)
    tribunal = models.ForeignKey(Tribunal, on_delete=models.SET_NULL, null=True)
    parquet = models.ForeignKey(Parquet, on_delete=models.SET_NULL, null=True, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    specialisation = models.CharField(max_length=100, blank=True)
    date_nomination = models.DateField()
    grade_siege = models.CharField(max_length=30, choices=GRADES_SIEGE, blank=True)
    grade_parquet = models.CharField(max_length=30, choices=GRADES_PARQUET, blank=True)
    
    def __str__(self):
        return f"Magistrat {self.utilisateur.get_full_name()}"
    
    class Meta:
        verbose_name = "Magistrat"
        verbose_name_plural = "Magistrats"


class Avocat(BaseModel):
    """Informations sur les avocats"""
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_barreau = models.CharField(max_length=50, unique=True)
    cabinet = models.CharField(max_length=200, blank=True)
    telephone = models.CharField(max_length=20)
    adresse = models.TextField()
    specialisation = models.CharField(max_length=100, blank=True)
    date_serment = models.DateField()
    barreau = models.CharField(max_length=100, help_text="Barreau de rattachement")
    
    def __str__(self):
        return f"Me {self.utilisateur.get_full_name()} - {self.numero_barreau}"
    
    class Meta:
        verbose_name = "Avocat"
        verbose_name_plural = "Avocats"


class Partie(BaseModel):
    """Parties à l'instance (demandeurs, défendeurs, etc.)"""
    TYPES_PARTIE = [
        ('DEMANDEUR', 'Demandeur'),
        ('DEFENDEUR', 'Défendeur'),
        ('REQUERANT', 'Requérant'),
        ('INTIME', 'Intimé'),
        ('APPELANT', 'Appelant'),
        ('APPELE', 'Appelé'),
        ('TEMOIN', 'Témoin'),
        ('PARTIE_CIVILE', 'Partie Civile'),
        ('PREVENU', 'Prévenu'),
        ('ACCUSE', 'Accusé'),
        ('TIERS', 'Tiers'),
        ('MINISTERE_PUBLIC', 'Ministère Public'),
        ('PROCUREUR', 'Procureur'),
        ('PARTIE_POURSUIVANTE', 'Partie Poursuivante'),
    ]
    
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    nom_usage = models.CharField(max_length=100, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    adresse = models.TextField()
    numero_identification = models.CharField(max_length=50, blank=True, 
                                           help_text="NIR, SIREN, SIRET, etc.")
    est_personne_morale = models.BooleanField(default=False)
    raison_sociale = models.CharField(max_length=200, blank=True)
    forme_juridique = models.CharField(max_length=100, blank=True, 
                                     help_text="SARL, SAS, Association, etc.")
    
    def __str__(self):
        if self.est_personne_morale:
            return self.raison_sociale
        return f"{self.prenom} {self.nom}"
    
    class Meta:
        verbose_name = "Partie"
        verbose_name_plural = "Parties"


class NatureAffaire(BaseModel):
    """Nature des affaires/types de procédures"""
    nom = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    matiere = models.CharField(max_length=50, choices=[
        ('CIVILE', 'Matière Civile'),
        ('PENALE', 'Matière Pénale'),
        ('COMMERCIALE', 'Matière Commerciale'),
        ('ADMINISTRATIVE', 'Matière Administrative'),
        ('SOCIALE', 'Matière Sociale'),
    ])
    
    def __str__(self):
        return f"{self.code} - {self.nom}"
    
    class Meta:
        verbose_name = "Nature d'Affaire"
        verbose_name_plural = "Natures d'Affaires"


class Dossier(BaseModel):
    """Dossier principal (affaire judiciaire)"""
    ETATS_DOSSIER = [
        ('ENREGISTRE', 'Enregistré'),
        ('INSTRUCTION', 'En Instruction'),
        ('MISE_EN_ETAT', 'Mise en État'),
        ('PRET_PLAIDOIRIE', 'Prêt pour Plaidoirie'),
        ('EN_DELIBERE', 'En Délibéré'),
        ('JUGE', 'Jugé'),
        ('CLOS', 'Clos'),
        ('RADIE', 'Radié'),
        ('DESISTEMENT', 'Désistement'),
        ('APPEL', 'Appelé'),
        ('POURVOI', 'Pourvoi en Cassation'),
        ('CLASSE_SANS_SUITE', 'Classé sans Suite'),
        ('RENVOI_CORRECTIONNEL', 'Renvoi Correctionnel'),
        ('RENVOI_ASSISES', 'Renvoi aux Assises'),
    ]
    
    DEGRES_URGENCE = [
        ('NORMALE', 'Normale'),
        ('URGENTE', 'Urgente'),
        ('TRES_URGENTE', 'Très Urgente'),
        ('REFERE', 'Référé'),
        ('FLAGRANT_DELIT', 'Flagrant Délit'),
    ]
    
    numero_rg = models.CharField(max_length=50, unique=True, 
                               help_text="Numéro de Répertoire Général")
    numero_parquet = models.CharField(max_length=50, blank=True,
                                    help_text="Numéro du parquet pour les affaires pénales")
    numero_instruction = models.CharField(max_length=50, blank=True,
                                        help_text="Numéro d'instruction")
    intitule = models.CharField(max_length=300)
    objet_litige = models.TextField()
    nature_affaire = models.ForeignKey(NatureAffaire, on_delete=models.PROTECT)
    tribunal = models.ForeignKey(Tribunal, on_delete=models.PROTECT)
    parquet = models.ForeignKey(Parquet, on_delete=models.SET_NULL, null=True, blank=True,
                               help_text="Parquet en charge pour les affaires pénales")
    magistrat_siege = models.ForeignKey(Magistrat, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='dossiers_siege')
    magistrat_parquet = models.ForeignKey(Magistrat, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='dossiers_parquet')
    etat = models.CharField(max_length=25, choices=ETATS_DOSSIER, default='ENREGISTRE')
    urgence = models.CharField(max_length=15, choices=DEGRES_URGENCE, default='NORMALE')
    date_enregistrement = models.DateField(default=timezone.now)
    date_cloture = models.DateField(null=True, blank=True)
    duree_estimee = models.IntegerField(help_text="Durée estimée en jours", null=True, blank=True)
    chambre = models.CharField(max_length=50, blank=True, help_text="Chambre ou section")
    est_confidentiel = models.BooleanField(default=False, help_text="Dossier sous secret")
    
    def __str__(self):
        return f"{self.numero_rg} - {self.intitule}"
    
    class Meta:
        verbose_name = "Dossier"
        verbose_name_plural = "Dossiers"


class PartieAuDossier(BaseModel):
    """Relation entre dossiers et parties"""
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='parties_dossier')
    partie = models.ForeignKey(Partie, on_delete=models.CASCADE)
    qualite = models.CharField(max_length=20, choices=Partie.TYPES_PARTIE)
    avocat = models.ForeignKey(Avocat, on_delete=models.SET_NULL, null=True, blank=True)
    date_constitution = models.DateField(default=timezone.now)
    observations = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['dossier', 'partie', 'qualite']
        verbose_name = "Partie au Dossier"
        verbose_name_plural = "Parties au Dossier"
    
    def __str__(self):
        return f"{self.dossier.numero_rg} - {self.partie} ({self.qualite})"


class Audience(BaseModel):
    """Audiences/séances"""
    TYPES_AUDIENCE = [
        ('PLAIDOIRIE', 'Plaidoirie'),
        ('MISE_EN_ETAT', 'Mise en État'),
        ('REFERE', 'Référé'),
        ('COMPARUTION', 'Comparution'),
        ('JUGEMENT', 'Jugement'),
        ('APPEL_CAUSE', 'Appel des Causes'),
        ('DELIBERE', 'Délibéré'),
        ('PRONONCE', 'Prononcé'),
        ('RENVOI', 'Renvoi'),
    ]
    
    ETATS_AUDIENCE = [
        ('PROGRAMMEE', 'Programmée'),
        ('EN_COURS', 'En Cours'),
        ('TERMINEE', 'Terminée'),
        ('REPORTEE', 'Reportée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='audiences')
    type_audience = models.CharField(max_length=20, choices=TYPES_AUDIENCE)
    date_prevue = models.DateTimeField()
    heure_debut_reelle = models.DateTimeField(null=True, blank=True)
    heure_fin_reelle = models.DateTimeField(null=True, blank=True)
    salle = models.CharField(max_length=50)
    magistrat = models.ForeignKey(Magistrat, on_delete=models.PROTECT)
    etat = models.CharField(max_length=20, choices=ETATS_AUDIENCE, default='PROGRAMMEE')
    observations = models.TextField(blank=True)
    est_publique = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.dossier.numero_rg} - {self.type_audience} le {self.date_prevue.strftime('%d/%m/%Y')}"
    
    class Meta:
        verbose_name = "Audience"
        verbose_name_plural = "Audiences"


class PieceJointe(BaseModel):
    """Pièces et documents du dossier"""
    TYPES_PIECE = [
        ('ASSIGNATION', 'Assignation'),
        ('CITATION', 'Citation'),
        ('REQUETE', 'Requête'),
        ('CONCLUSIONS', 'Conclusions'),
        ('MEMOIRE', 'Mémoire'),
        ('ORDONNANCE', 'Ordonnance'),
        ('JUGEMENT', 'Jugement'),
        ('ARRET', 'Arrêt'),
        ('PIECE_COMMUNICATION', 'Pièce de Communication'),
        ('EXPERTISE', 'Expertise'),
        ('ENQUETE', 'Enquête'),
        ('PV_CONCILIATION', 'PV de Conciliation'),
        ('TRANSACTION', 'Transaction'),
        ('APPEL', 'Acte d\'Appel'),
        ('POURVOI', 'Pourvoi'),
        ('AUTRE', 'Autre'),
    ]
    
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='pieces_jointes')
    titre = models.CharField(max_length=200)
    type_piece = models.CharField(max_length=25, choices=TYPES_PIECE)
    fichier = models.FileField(upload_to='pieces_dossier/')
    depose_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_depot = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    est_confidentielle = models.BooleanField(default=False)
    numero_piece = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.dossier.numero_rg} - {self.titre}"
    
    class Meta:
        verbose_name = "Pièce Jointe"
        verbose_name_plural = "Pièces Jointes"


class Note(BaseModel):
    """Notes et observations sur le dossier"""
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='notes')
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    contenu = models.TextField()
    est_publique = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Note"
        verbose_name_plural = "Notes"
    
    def __str__(self):
        return f"{self.dossier.numero_rg} - Note de {self.auteur.username if self.auteur else 'Inconnu'}"


class Frais(BaseModel):
    """Frais de justice et paiements"""
    TYPES_FRAIS = [
        ('DROIT_GREFFE', 'Droit de Greffe'),
        ('TIMBRE_FISCAL', 'Timbre Fiscal'), 
        ('CONSIGNATION', 'Consignation'),
        ('EXPERTISE', 'Frais d\'Expertise'),
        ('SIGNIFICATION', 'Frais de Signification'),
        ('AMENDE', 'Amende'),
        ('DOMMAGES_INTERETS', 'Dommages et Intérêts'),
        ('DEPENS', 'Dépens'),
        ('AUTRE', 'Autre'),
    ]
    
    ETATS_PAIEMENT = [
        ('A_PAYER', 'À Payer'),
        ('PAYE', 'Payé'),
        ('PARTIEL', 'Partiellement Payé'),
        ('EN_RETARD', 'En Retard'),
        ('EXONERE', 'Exonéré'),
    ]
    
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='frais')
    type_frais = models.CharField(max_length=20, choices=TYPES_FRAIS)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_echeance = models.DateField()
    date_paiement = models.DateField(null=True, blank=True)
    etat = models.CharField(max_length=15, choices=ETATS_PAIEMENT, default='A_PAYER')
    mode_paiement = models.CharField(max_length=50, blank=True)
    numero_recu = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.dossier.numero_rg} - {self.type_frais}: {self.montant}€"
    
    class Meta:
        verbose_name = "Frais"
        verbose_name_plural = "Frais"


class RequisitionParquet(BaseModel):
    """Réquisitions du parquet"""
    TYPES_REQUISITION = [
        ('POURSUITE', 'Réquisition de Poursuite'),
        ('NON_LIEU', 'Réquisition de Non-lieu'),
        ('CLASSEMENT', 'Réquisition de Classement'),
        ('PEINE', 'Réquisition de Peine'),
        ('MESURE_SURETE', 'Réquisition de Mesure de Sûreté'),
        ('MISE_EXAMEN', 'Réquisition de Mise en Examen'),
        ('MANDAT', 'Réquisition de Mandat'),
        ('PERQUISITION', 'Réquisition de Perquisition'),
        ('EXPERTISE', 'Réquisition d\'Expertise'),
    ]
    
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='requisitions')
    parquet = models.ForeignKey(Parquet, on_delete=models.CASCADE)
    magistrat_parquet = models.ForeignKey(Magistrat, on_delete=models.CASCADE)
    type_requisition = models.CharField(max_length=20, choices=TYPES_REQUISITION)
    contenu = models.TextField(help_text="Contenu de la réquisition")
    date_requisition = models.DateField(default=timezone.now)
    est_suivie = models.BooleanField(default=False, help_text="Réquisition suivie par le juge")
    observations = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.dossier.numero_rg} - {self.type_requisition}"
    
    class Meta:
        verbose_name = "Réquisition du Parquet"
        verbose_name_plural = "Réquisitions du Parquet"


class ProcedureEnquete(BaseModel):
    """Procédures d'enquête dirigées par le parquet"""
    TYPES_ENQUETE = [
        ('PRELIMINAIRE', 'Enquête Preliminaire'),
        ('FLAGRANCE', 'Enquête de Flagrance'),
        ('COMMISSION_ROGATOIRE', 'Commission Rogatoire'),
        ('INFORMATION_JUDICIAIRE', 'Information Judiciaire'),
    ]
    
    ETATS_ENQUETE = [
        ('EN_COURS', 'En Cours'),
        ('TERMINEE', 'Terminée'),
        ('SUSPENDUE', 'Suspendue'),
        ('CLASSEE', 'Classée'),
    ]
    
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='enquetes')
    parquet = models.ForeignKey(Parquet, on_delete=models.CASCADE)
    magistrat_parquet = models.ForeignKey(Magistrat, on_delete=models.CASCADE)
    type_enquete = models.CharField(max_length=25, choices=TYPES_ENQUETE)
    officier_police_judiciaire = models.CharField(max_length=200, help_text="OPJ en charge")
    service_enqueteur = models.CharField(max_length=200, help_text="Service de police/gendarmerie")
    date_ouverture = models.DateField(default=timezone.now)
    date_cloture = models.DateField(null=True, blank=True)
    etat_enquete = models.CharField(max_length=15, choices=ETATS_ENQUETE, default='EN_COURS')
    synthese = models.TextField(blank=True, help_text="Synthèse de l'enquête")
    
    def __str__(self):
        return f"{self.dossier.numero_rg} - {self.type_enquete}"
    
    class Meta:
        verbose_name = "Procédure d'Enquête"
        verbose_name_plural = "Procédures d'Enquête"


class Classement(BaseModel):
    """Décisions de classement du parquet"""
    MOTIFS_CLASSEMENT = [
        ('SANS_SUITE_CHARGES_INSUFFISANTES', 'Charges Insuffisantes'),
        ('SANS_SUITE_AUTEUR_INCONNU', 'Auteur Inconnu'),
        ('SANS_SUITE_INFRACTION_INEXISTANTE', 'Infraction Inexistante'),
        ('SANS_SUITE_AMNISTIE', 'Amnistie'),
        ('SANS_SUITE_PRESCRIPTION', 'Prescription'),
        ('SANS_SUITE_DECES', 'Décès de l\'Auteur'),
        ('SANS_SUITE_OPPORTUNITE', 'Inopportunité des Poursuites'),
        ('SANS_SUITE_TRANSACTION', 'Transaction'),
        ('SANS_SUITE_MEDIATION', 'Médiation Pénale'),
        ('SANS_SUITE_RAPPEL_LOI', 'Rappel à la Loi'),
    ]
    
    dossier = models.OneToOneField(Dossier, on_delete=models.CASCADE, related_name='classement')
    parquet = models.ForeignKey(Parquet, on_delete=models.CASCADE)
    magistrat_parquet = models.ForeignKey(Magistrat, on_delete=models.CASCADE)
    motif_classement = models.CharField(max_length=40, choices=MOTIFS_CLASSEMENT)
    date_classement = models.DateField(default=timezone.now)
    motivation = models.TextField(help_text="Motivation détaillée du classement")
    notifie_parties = models.BooleanField(default=False)
    date_notification = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"Classement {self.dossier.numero_rg} - {self.motif_classement}"
    
    class Meta:
        verbose_name = "Classement"
        verbose_name_plural = "Classements"


class AlternativePoursuites(BaseModel):
    """Alternatives aux poursuites proposées par le parquet"""
    TYPES_ALTERNATIVE = [
        ('MEDIATION_PENALE', 'Médiation Pénale'),
        ('COMPOSITION_PENALE', 'Composition Pénale'),
        ('RAPPEL_LOI', 'Rappel à la Loi'),
        ('AVERTISSEMENT', 'Avertissement'),
        ('STAGE_CITOYENNETE', 'Stage de Citoyenneté'),
        ('TRAVAIL_INTERET_GENERAL', 'Travail d\'Intérêt Général'),
        ('REPARATION', 'Mesure de Réparation'),
        ('INJONCTION_THERAPEUTIQUE', 'Injonction Thérapeutique'),
    ]
    
    ETATS_ALTERNATIVE = [
        ('PROPOSEE', 'Proposée'),
        ('ACCEPTEE', 'Acceptée'),
        ('REFUSEE', 'Refusée'),
        ('EN_COURS', 'En Cours d\'Exécution'),
        ('EXECUTEE', 'Exécutée'),
        ('NON_EXECUTEE', 'Non Exécutée'),
    ]
    
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='alternatives')
    parquet = models.ForeignKey(Parquet, on_delete=models.CASCADE)
    magistrat_parquet = models.ForeignKey(Magistrat, on_delete=models.CASCADE, related_name='alternatives_as_parquet')
    type_alternative = models.CharField(max_length=25, choices=TYPES_ALTERNATIVE)
    date_proposition = models.DateField(default=timezone.now)
    date_acceptation = models.DateField(null=True, blank=True)
    date_execution = models.DateField(null=True, blank=True)
    etat = models.CharField(max_length=15, choices=ETATS_ALTERNATIVE, default='PROPOSEE')
    modalites = models.TextField(help_text="Modalités d'exécution")
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                 help_text="Montant en cas d'amende de composition")
    
    def __str__(self):
        return f"{self.dossier.numero_rg} - {self.type_alternative}"
    
    class Meta:
        verbose_name = "Alternative aux Poursuites"
        verbose_name_plural = "Alternatives aux Poursuites"
    """Calendrier des audiences"""
    date = models.DateField()
    tribunal = models.ForeignKey(Tribunal, on_delete=models.CASCADE)
    magistrat = models.ForeignKey(Magistrat, on_delete=models.CASCADE,
        related_name='alternatives_as_magistrat')
    est_disponible = models.BooleanField(default=True)
    observations = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['date', 'tribunal', 'magistrat']
        verbose_name = "Calendrier"
        verbose_name_plural = "Calendriers"
    
    def __str__(self):
        return f"{self.tribunal.nom} - {self.magistrat.utilisateur.get_full_name()} - {self.date}"


class Attribution(BaseModel):
    """Attribution de dossiers au personnel"""
    TYPES_ATTRIBUTION = [
        ('GREFFIER', 'Greffier'),
        ('GREFFIER_CHEF', 'Greffier en Chef'),
        ('SECRETAIRE', 'Secrétaire'),
        ('HUISSIER', 'Huissier'),
        ('AUTRE', 'Autre'),
    ]
    
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='attributions')
    attribue_a = models.ForeignKey(User, on_delete=models.CASCADE)
    type_attribution = models.CharField(max_length=20, choices=TYPES_ATTRIBUTION)
    date_attribution = models.DateField(default=timezone.now)
    observations = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.dossier.numero_rg} - {self.attribue_a.get_full_name()} ({self.type_attribution})"
    
    class Meta:
        verbose_name = "Attribution"
        verbose_name_plural = "Attributions"


class VoieRecours(BaseModel):
    """Voies de recours (appel, cassation, etc.)"""
    TYPES_RECOURS = [
        ('APPEL', 'Appel'),
        ('POURVOI_CASSATION', 'Pourvoi en Cassation'),
        ('OPPOSITION', 'Opposition'),
        ('TIERCE_OPPOSITION', 'Tierce Opposition'),
        ('RECOURS_REVISION', 'Recours en Révision'),
    ]
    
    ETATS_RECOURS = [
        ('FORME', 'Formé'),
        ('INSTRUIT', 'En Instruction'),
        ('ADMIS', 'Admis'),
        ('REJETE', 'Rejeté'),
        ('IRRECEVABLE', 'Irrecevable'),
        ('DESISTEMENT', 'Désistement'),
    ]
    
    dossier_origine = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='recours_formes')
    dossier_recours = models.OneToOneField(Dossier, on_delete=models.CASCADE, related_name='info_recours')
    type_recours = models.CharField(max_length=20, choices=TYPES_RECOURS)
    tribunal_recours = models.ForeignKey(Tribunal, on_delete=models.PROTECT)
    date_formation = models.DateField(default=timezone.now)
    etat = models.CharField(max_length=15, choices=ETATS_RECOURS, default='FORME')
    motifs = models.TextField(help_text="Motifs du recours")
    
    def __str__(self):
        return f"{self.type_recours} - {self.dossier_origine.numero_rg}"
    
    class Meta:
        verbose_name = "Voie de Recours"
        verbose_name_plural = "Voies de Recours"


class Decision(BaseModel):
    """Décisions de justice"""
    TYPES_DECISION = [
        ('JUGEMENT', 'Jugement'),
        ('ARRET', 'Arrêt'),
        ('ORDONNANCE', 'Ordonnance'),
        ('SENTENCE', 'Sentence Arbitrale'),
    ]
    
    SENS_DECISION = [
        ('ACCUEIL', 'Accueil'),
        ('REJET', 'Rejet'),
        ('PARTIEL', 'Accueil Partiel'),
        ('DESISTEMENT', 'Désistement'),
        ('IRRECEVABLE', 'Irrecevabilité'),
    ]
    
    dossier = models.OneToOneField(Dossier, on_delete=models.CASCADE, related_name='decision')
    type_decision = models.CharField(max_length=15, choices=TYPES_DECISION)
    numero_decision = models.CharField(max_length=50, unique=True)
    date_decision = models.DateField()
    date_lecture = models.DateField(null=True, blank=True)
    sens_decision = models.CharField(max_length=15, choices=SENS_DECISION)
    dispositif = models.TextField(help_text="Dispositif de la décision")
    motifs = models.TextField(help_text="Motifs de la décision")
    est_contradictoire = models.BooleanField(default=True)
    est_executoire = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.type_decision} n°{self.numero_decision} - {self.dossier.numero_rg}"
    
    class Meta:
        verbose_name = "Décision"
        verbose_name_plural = "Décisions"


class Scelle(BaseModel):
    """Gestion des scellés et pièces à conviction"""
    TYPES_SCELLE = [
        ('PIECE_CONVICTION', 'Pièce à Conviction'),
        ('DOCUMENT_SAISI', 'Document Saisi'),
        ('OBJET_SEQUESTRE', 'Objet Séquestré'),
        ('PREUVE_MATERIELLE', 'Preuve Matérielle'),
        ('AUTRE', 'Autre'),
    ]
    
    dossier = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='scelles')
    numero_scelle = models.CharField(max_length=50)
    type_scelle = models.CharField(max_length=20, choices=TYPES_SCELLE)
    description = models.TextField()
    date_saisie = models.DateField()
    saisi_par = models.CharField(max_length=100)
    lieu_conservation = models.CharField(max_length=200, blank=True)
    chaine_possession = models.TextField(blank=True, help_text="Chaîne de possession/custody")
    est_verse_debats = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['dossier', 'numero_scelle']
        verbose_name = "Scellé"
        verbose_name_plural = "Scellés"
    
    def __str__(self):
        return f"{self.dossier.numero_rg} - Scellé n°{self.numero_scelle}"