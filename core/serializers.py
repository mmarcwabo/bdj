import uuid
from rest_framework import serializers
from .models import (
    Tribunal, Parquet, Magistrat, Avocat, Partie, NatureAffaire, Dossier,
    PartieAuDossier, Audience, PieceJointe, Note, Frais, RequisitionParquet,
    ProcedureEnquete, Classement, AlternativePoursuites,
    Attribution, VoieRecours, Decision, Scelle
)

from django.contrib.auth.models import User
from django.db import models


class Calendrier(models.Model): # Placeholder if not fully defined in models.py
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    est_actif = models.BooleanField(default=True)
    date = models.DateField()
    tribunal = models.ForeignKey(Tribunal, on_delete=models.CASCADE)
    magistrat = models.ForeignKey(Magistrat, on_delete=models.CASCADE, related_name='alternatives_as_magistrat_calendar_custom') # custom to avoid conflict
    est_disponible = models.BooleanField(default=True)
    observations = models.TextField(blank=True)

    class Meta:
        unique_together = ['date', 'tribunal', 'magistrat']
        verbose_name = "Calendrier"
        verbose_name_plural = "Calendriers"

    def __str__(self):
        return f"{self.tribunal.nom} - {self.magistrat.utilisateur.get_full_name()} - {self.date}"


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class TribunalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tribunal
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class ParquetSerializer(serializers.ModelSerializer):
    tribunal_details = TribunalSerializer(source='tribunal', read_only=True) # For richer display

    class Meta:
        model = Parquet
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class MagistratSerializer(serializers.ModelSerializer):
    utilisateur_details = UserSerializer(source='utilisateur', read_only=True)
    tribunal_details = TribunalSerializer(source='tribunal', read_only=True, allow_null=True)
    parquet_details = ParquetSerializer(source='parquet', read_only=True, allow_null=True)

    class Meta:
        model = Magistrat
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class AvocatSerializer(serializers.ModelSerializer):
    utilisateur_details = UserSerializer(source='utilisateur', read_only=True)

    class Meta:
        model = Avocat
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class PartieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partie
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class NatureAffaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureAffaire
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class DossierSerializer(serializers.ModelSerializer):
    nature_affaire_details = NatureAffaireSerializer(source='nature_affaire', read_only=True)
    tribunal_details = TribunalSerializer(source='tribunal', read_only=True)
    parquet_details = ParquetSerializer(source='parquet', read_only=True, allow_null=True)
    magistrat_siege_details = MagistratSerializer(source='magistrat_siege', read_only=True, allow_null=True)
    magistrat_parquet_details = MagistratSerializer(source='magistrat_parquet', read_only=True, allow_null=True)


    class Meta:
        model = Dossier
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class PartieAuDossierSerializer(serializers.ModelSerializer):
    dossier_details = DossierSerializer(source='dossier', read_only=True)
    partie_details = PartieSerializer(source='partie', read_only=True)
    avocat_details = AvocatSerializer(source='avocat', read_only=True, allow_null=True)
    # For write operations
    dossier = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all())
    partie = serializers.PrimaryKeyRelatedField(queryset=Partie.objects.all())
    avocat = serializers.PrimaryKeyRelatedField(queryset=Avocat.objects.all(), allow_null=True, required=False)


    class Meta:
        model = PartieAuDossier
        fields = '__all__' # This will include both PK fields and detail fields. Adjust as needed.
        read_only_fields = ('id', 'date_creation', 'date_modification')
        # To avoid sending both 'dossier' (PK) and 'dossier_details' (nested),
        # you might have separate serializers for read and write, or customize fields.
        # Thanks to Gemini

class AudienceSerializer(serializers.ModelSerializer):
    dossier_details = DossierSerializer(source='dossier', read_only=True)
    magistrat_details = MagistratSerializer(source='magistrat', read_only=True)
    dossier = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all())
    magistrat = serializers.PrimaryKeyRelatedField(queryset=Magistrat.objects.all())

    class Meta:
        model = Audience
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class PieceJointeSerializer(serializers.ModelSerializer):
    dossier_details = DossierSerializer(source='dossier', read_only=True)
    depose_par_details = UserSerializer(source='depose_par', read_only=True, allow_null=True)
    dossier = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all())
    depose_par = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)

    class Meta:
        model = PieceJointe
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification', 'date_depot') # date_depot is auto_now_add

class NoteSerializer(serializers.ModelSerializer):
    dossier_details = DossierSerializer(source='dossier', read_only=True)
    auteur_details = UserSerializer(source='auteur', read_only=True, allow_null=True)
    dossier = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all())
    auteur = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class FraisSerializer(serializers.ModelSerializer):
    dossier_details = DossierSerializer(source='dossier', read_only=True)
    dossier = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all())

    class Meta:
        model = Frais
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class RequisitionParquetSerializer(serializers.ModelSerializer):
    dossier_details = DossierSerializer(source='dossier', read_only=True)
    parquet_details = ParquetSerializer(source='parquet', read_only=True)
    magistrat_parquet_details = MagistratSerializer(source='magistrat_parquet', read_only=True)
    dossier = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all())
    parquet = serializers.PrimaryKeyRelatedField(queryset=Parquet.objects.all())
    magistrat_parquet = serializers.PrimaryKeyRelatedField(queryset=Magistrat.objects.filter(type_magistrat='PARQUET'))


    class Meta:
        model = RequisitionParquet
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class ProcedureEnqueteSerializer(serializers.ModelSerializer):
    dossier_details = DossierSerializer(source='dossier', read_only=True)
    parquet_details = ParquetSerializer(source='parquet', read_only=True)
    magistrat_parquet_details = MagistratSerializer(source='magistrat_parquet', read_only=True)
    dossier = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all())
    parquet = serializers.PrimaryKeyRelatedField(queryset=Parquet.objects.all())
    magistrat_parquet = serializers.PrimaryKeyRelatedField(queryset=Magistrat.objects.filter(type_magistrat='PARQUET'))

    class Meta:
        model = ProcedureEnquete
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class ClassementSerializer(serializers.ModelSerializer):
    dossier_details = DossierSerializer(source='dossier', read_only=True)
    parquet_details = ParquetSerializer(source='parquet', read_only=True)
    magistrat_parquet_details = MagistratSerializer(source='magistrat_parquet', read_only=True)
    dossier = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all()) # For OneToOne, this is fine for write
    parquet = serializers.PrimaryKeyRelatedField(queryset=Parquet.objects.all())
    magistrat_parquet = serializers.PrimaryKeyRelatedField(queryset=Magistrat.objects.filter(type_magistrat='PARQUET'))


    class Meta:
        model = Classement
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class AlternativePoursuitesSerializer(serializers.ModelSerializer):
    dossier_details = DossierSerializer(source='dossier', read_only=True)
    parquet_details = ParquetSerializer(source='parquet', read_only=True)
    magistrat_parquet_details = MagistratSerializer(source='magistrat_parquet', read_only=True)
    dossier = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all())
    parquet = serializers.PrimaryKeyRelatedField(queryset=Parquet.objects.all())
    magistrat_parquet = serializers.PrimaryKeyRelatedField(queryset=Magistrat.objects.filter(type_magistrat='PARQUET'), source='magistrat_parquet')


    class Meta:
        model = AlternativePoursuites
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class CalendrierSerializer(serializers.ModelSerializer):
    tribunal_details = TribunalSerializer(source='tribunal', read_only=True)
    magistrat_details = MagistratSerializer(source='magistrat', read_only=True)
    tribunal = serializers.PrimaryKeyRelatedField(queryset=Tribunal.objects.all())
    magistrat = serializers.PrimaryKeyRelatedField(queryset=Magistrat.objects.all())

    class Meta:
        model = Calendrier
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')


class AttributionSerializer(serializers.ModelSerializer):
    dossier_details = DossierSerializer(source='dossier', read_only=True)
    attribue_a_details = UserSerializer(source='attribue_a', read_only=True)
    dossier = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all())
    attribue_a = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Attribution
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class VoieRecoursSerializer(serializers.ModelSerializer):
    dossier_origine_details = DossierSerializer(source='dossier_origine', read_only=True)
    dossier_recours_details = DossierSerializer(source='dossier_recours', read_only=True) # For OneToOne
    tribunal_recours_details = TribunalSerializer(source='tribunal_recours', read_only=True)
    dossier_origine = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all())
    dossier_recours = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all()) # For OneToOne, this is fine for write
    tribunal_recours = serializers.PrimaryKeyRelatedField(queryset=Tribunal.objects.all())


    class Meta:
        model = VoieRecours
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class DecisionSerializer(serializers.ModelSerializer):
    dossier_details = DossierSerializer(source='dossier', read_only=True) # For OneToOne
    dossier = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all()) # For OneToOne

    class Meta:
        model = Decision
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')

class ScelleSerializer(serializers.ModelSerializer):
    dossier_details = DossierSerializer(source='dossier', read_only=True)
    dossier = serializers.PrimaryKeyRelatedField(queryset=Dossier.objects.all())

    class Meta:
        model = Scelle
        fields = '__all__'
        read_only_fields = ('id', 'date_creation', 'date_modification')
