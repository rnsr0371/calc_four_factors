from django.db import models

# Create your models here.
#teamsテーブル
class Team(models.Model):
    teamname=models.CharField(max_length=100)

#ベーシックスタッツテーブル
class BasicStat(models.Model):
    team_id=models.ForeignKey(Team,on_delete=models.CASCADE)
    #game_id=models.IntegerField()#自動でIDが触れられるので不要
    PTS=models.IntegerField()
    F3GA=models.IntegerField()
    F3GM=models.IntegerField()
    F2GA=models.IntegerField()
    F2GM=models.IntegerField()
    FTA=models.IntegerField()
    FTM=models.IntegerField()
    ORB=models.IntegerField()
    DRB=models.IntegerField()
    TOV=models.IntegerField()

#Four Factorsテーブル
class Four_Factor(models.Model):
    game_id=models.ForeignKey(BasicStat,on_delete=models.CASCADE)
    team_id=models.ForeignKey(Team,on_delete=models.CASCADE)
    PPP=models.DecimalField(max_digits=5,decimal_places=2)
    POSS=models.DecimalField(max_digits=5,decimal_places=2)
    eFG=models.DecimalField(max_digits=5,decimal_places=2)
    TOV_Percentage=models.DecimalField(max_digits=5,decimal_places=2)
    ORB_Percentage=models.DecimalField(max_digits=5,decimal_places=2)
    FTR=models.DecimalField(max_digits=5,decimal_places=2)

