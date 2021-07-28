from django.shortcuts import render
from django.http import HttpResponse,HttpResponseServerError
from django.shortcuts import redirect
from .forms import CalcForm
from .models import BasicStat,Team,Four_Factor
from django.db.models import Max


#four factorsを計算する関数を定義する
def calc_PPP(PTS, POSS):
    PPP=PTS/POSS
    return PPP

def calc_POSS(F2GA,F3GA,FTA,TOV):
    POSS=F2GA+F3GA+0.44*FTA+TOV
    return POSS

def calc_eFG(F2GM,F3GM,F2GA,F3GA):
    eFG=((F2GM+F3GM)+0.5*F3GM)/(F2GA+F3GA)
    return eFG

def calc_TOVp(TOV,F2GA,F3GA,FTA):
    TOVp=TOV/((F2GA+F3GA)+0.44*FTA+TOV)
    return TOVp

def calc_FTR(FTA,F2GA,F3GA):
    FTR=FTA/(F2GA+F3GA)
    return FTR

def calc_ORBp(ORB,ORB_opp):
    ORBp=ORB/(ORB+ORB_opp)
    return ORBp



# Create your views here.
def index(request):
    params={
        "title":"Four Factorsを計算するアプリ",
        "form":CalcForm(),
    }

    if (request.method == "POST"):
        
        return redirect(to="result")
        #return render(request,"result.html")

    return render(request,"index.html",params)


def result(request):
    index=Four_Factor.objects.all().aggregate(Max("game_id"))["game_id__max"]

    #自チームのFour Factorsを呼び出す。
    team=Four_Factor.objects.get(game_id=index-1)
    
    #チーム名
    teamname=team.team_id.teamname
    #Four Factors
    POSS=team.POSS
    PPP=team.PPP
    eFG=team.eFG
    TOVp=team.TOV_Percentage
    ORBp=team.ORB_Percentage
    FTR=team.FTR

    #相手チームのFour Factorsを呼び出す。
    opp=Four_Factor.objects.get(game_id=index)
    #相手チーム名
    opp_name=opp.team_id.teamname
    #Four Factors
    POSS_opp=opp.POSS
    PPP_opp=opp.PPP
    eFG_opp=opp.eFG
    TOVp_opp=opp.TOV_Percentage
    ORBp_opp=opp.ORB_Percentage
    FTR_opp=opp.FTR


    params={
        "title":"Four Factorsを計算するアプリ",
        "teamname":teamname,
        "POSS":POSS,
        "PPP":PPP,
        "eFG":eFG,
        "TOVp":TOVp,
        "ORBp":ORBp,
        "FTR":FTR,

        "opponent":opp_name,
        "POSS_opp":POSS_opp,
        "PPP_opp":PPP_opp,
        "eFG_opp":eFG_opp,
        "TOVp_opp":TOVp_opp,
        "ORBp_opp":ORBp_opp,
        "FTR_opp":FTR_opp,
    }
    return render(request,"result.html",params)