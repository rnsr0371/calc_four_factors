from django import forms

class CalcForm(forms.Form):
    #自チーム
    team=forms.CharField(label="自チーム")
    PTS=forms.IntegerField(label="PTS",min_value=1)
    F3GA=forms.IntegerField(label="F3GA",min_value=1)
    F3GM=forms.IntegerField(label="F3GM",min_value=1)
    F2GA=forms.IntegerField(label="F2GA",min_value=1)
    F2GM=forms.IntegerField(label="F2GM",min_value=1)
    FTA=forms.IntegerField(label="FTA",min_value=1)
    FTM=forms.IntegerField(label="FTM",min_value=1)
    ORB=forms.IntegerField(label="ORB",min_value=1)
    DRB=forms.IntegerField(label="DRB",min_value=1)
    TOV=forms.IntegerField(label="TOV",min_value=1)

    #相手チーム
    opponent=forms.CharField(label="相手チーム")
    PTS_opp=forms.IntegerField(label="PTS_opp",min_value=1)
    F3GA_opp=forms.IntegerField(label="F3GA_opp",min_value=1)
    F3GM_opp=forms.IntegerField(label="F3GM_opp",min_value=1)
    F2GA_opp=forms.IntegerField(label="F2GA_opp",min_value=1)
    F2GM_opp=forms.IntegerField(label="F2GM_opp",min_value=1)
    FTA_opp=forms.IntegerField(label="FTA_opp",min_value=1)
    FTM_opp=forms.IntegerField(label="FTM_opp",min_value=1)
    ORB_opp=forms.IntegerField(label="ORB_opp",min_value=1)
    DRB_opp=forms.IntegerField(label="DRB_opp",min_value=1)
    TOV_opp=forms.IntegerField(label="TOV_opp",min_value=1)
