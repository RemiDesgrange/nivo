
function ChangeOnglet(onglet) 
{   
    contenu="BSHenneigements_graph_" + onglet;
    document.getElementById('BSHenneigements_graph_alt1').style.display = 'none';
    document.getElementById('BSHenneigements_graph_alt2').style.display = 'none';
    document.getElementById('BSHenneigements_graph_alt3').style.display = 'none';       
    document.getElementById('BSHenneigements_graph_nord').style.display = 'none';       
    document.getElementById('BSHenneigements_graph_sud').style.display = 'none';       
    document.getElementById('BSHenneigements_graph_limite').style.display = 'none';       
    document.getElementById(contenu).style.display = 'block';       
    
    onglet="BSHenneigements_tab_"+onglet
    document.getElementById('BSHenneigements_tab_alt1').className = '';
    document.getElementById('BSHenneigements_tab_alt2').className = '';
    document.getElementById('BSHenneigements_tab_alt3').className = '';       
    document.getElementById('BSHenneigements_tab_nord').className = '';       
    document.getElementById('BSHenneigements_tab_sud').className = '';       
    document.getElementById('BSHenneigements_tab_limite').className = '';       
    document.getElementById(onglet).className = 'active';       
}    