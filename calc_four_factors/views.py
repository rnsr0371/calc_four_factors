from django.shortcuts import render
from django.http import HttpResponse,HttpResponseServerError
from django.shortcuts import redirect
from .forms import CalcForm
from .models import BasicStat,Team,Four_Factor
from django.db.models import Max

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import io

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

#レーダーチャートを描く関数を定義する
def write_graph(eFG,TOVp,FTR,ORBp):
    values=np.array([eFG,TOVp,FTR,ORBp])
    labels=["eFG","TOV%","FTR","ORB%"]

    #多角形を閉じるためにデータの最後に最初の値を追加する
    radar_values=np.concatenate([values,[values[0]]])

    #プロットする角度を形成する
    angles=np.linspace(0,2*np.pi,len(labels)+1,endpoint=True)
    fig=plt.figure(facecolor="w")
    
    ax=fig.add_subplot(1,1,1,polar=True)
    ax.plot(angles,radar_values)
    ax.fill(angles,radar_values,alpha=0.2)
    ax.set_thetagrid(angles[:-1]*180/np.pi,labels)

    ax.set_title("Four Factors",pad=20)

#SVG化
def plt2svg():
    buf=io.BytesIO()
    plt.savefig(buf,format="svg",bbox_inches="tihgt")
    s=buf.getvalue()
    buf.close()

    return s






# Create your views here.
def index(request):
    params={
        "title":"Four Factorsを計算するアプリ",
        "form":CalcForm(),
    }

    if (request.method == "POST"):
        #自チーム
        team=request.POST["team"]
        PTS=int(request.POST["PTS"])
        F3GA=int(request.POST["F3GA"])
        F3GM=int(request.POST["F3GM"])
        F2GA=int(request.POST["F2GA"])
        F2GM=int(request.POST["F2GM"])
        FTA=int(request.POST["FTA"])
        FTM=int(request.POST["FTM"])
        ORB=int(request.POST["ORB"])
        DRB=int(request.POST["DRB"])
        TOV=int(request.POST["TOV"])

        #相手チーム
        opponent=request.POST["opponent"]
        PTS_opp=int(request.POST["PTS_opp"])
        F3GA_opp=int(request.POST["F3GA_opp"])
        F3GM_opp=int(request.POST["F3GM_opp"])
        F2GA_opp=int(request.POST["F2GA_opp"])
        F2GM_opp=int(request.POST["F2GM_opp"])
        FTA_opp=int(request.POST["FTA_opp"])
        FTM_opp=int(request.POST["FTM_opp"])
        ORB_opp=int(request.POST["ORB_opp"])
        DRB_opp=int(request.POST["DRB_opp"])
        TOV_opp=int(request.POST["TOV_opp"])

        #自チームをTeamsに登録
        teams=Team(teamname=team)
        teams.save()

        #自チームのスタッツをBasicStatsに登録
        basic_stats=BasicStat(team_id=Team.objects.order_by("id").last(),
        PTS=PTS,F3GA=F3GA,F3GM=F3GM,F2GA=F2GA,F2GM=F2GM,FTA=FTA,FTM=FTM,ORB=ORB,DRB=DRB,TOV=TOV)
        basic_stats.save()

        #自チームのfour factorsを計算
        POSS=calc_POSS(F2GA,F3GA,FTA,TOV)
        PPP=calc_PPP(PTS,POSS)

        eFG=calc_eFG(F2GM,F3GM,F2GA,F3GA)
        TOVp=calc_TOVp(TOV,F2GA,F3GA,FTA)
        FTR=calc_FTR(FTA,F2GA,F3GA)
        ORBp=calc_ORBp(ORB,ORB_opp)

        #計算したfour factorsをfour factorに登録
        four_factors=Four_Factor(game_id=BasicStat.objects.order_by("id").last(),
        team_id=Team.objects.order_by("id").last(),
        PPP=PPP,POSS=POSS,eFG=eFG,TOV_Percentage=TOVp,ORB_Percentage=ORBp,FTR=FTR)

        four_factors.save()
        

        #相手チームをTeamsに登録
        teams=Team(teamname=opponent)
        teams.save()

        #相手チームのスタッツをBasicStatsに登録 
        basic_stats=BasicStat(team_id=Team.objects.order_by("id").last(),
        PTS=PTS_opp,F3GA=F3GA_opp,F3GM=F3GM_opp,F2GA=F2GA_opp,F2GM=F2GM_opp,FTA=FTA_opp,FTM=FTM_opp,ORB=ORB_opp,DRB=DRB_opp,TOV=TOV_opp)
        basic_stats.save()      

        #相手チームのfour factorsを計算
        POSS_opp=calc_POSS(F2GA_opp,F3GA_opp,FTA_opp,TOV_opp)
        PPP_opp=calc_PPP(PTS_opp,POSS_opp)

        eFG_opp=calc_eFG(F2GM_opp,F3GM_opp,F2GA_opp,F3GA_opp)
        TOVp_opp=calc_TOVp(TOV_opp,F2GA_opp,F3GA_opp,FTA_opp)
        FTR_opp=calc_FTR(FTA_opp,F2GA_opp,F3GA_opp)
        ORBp_opp=calc_ORBp(ORB_opp,ORB)

        #計算したfour factorsをfour factorに登録
        four_factors=Four_Factor(game_id=BasicStat.objects.order_by("id").last(),
        team_id=Team.objects.order_by("id").last(),
        PPP=PPP_opp,POSS=POSS_opp,eFG=eFG_opp,TOV_Percentage=TOVp_opp,ORB_Percentage=ORBp_opp,FTR=FTR_opp)
        four_factors.save()

        return(redirect(to="calc_four_factors/result"))

    return render(request,"calc_four_factors/index.html",params)


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

    #write_graph(eFG,TOVp,FTR,ORBp)
    #svg=plt2svg()
    #plt.cla()
    #response=HttpResponse(svg,content_type="image/svg+xml")

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

        #"response":response,#レーダーチャート

    }
    return render(request,"calc_four_factors/result.html",params)

#@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)