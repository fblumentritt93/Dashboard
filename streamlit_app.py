import streamlit as st
import pandas as pd
from PIL import Image
import plost
import json
import base64

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def to_percentage(value):
    #v1 = "{:,.2f}".format(value * 100).replace('.', ',')
    v1 = f'{value*100:,.2f} %'
    v2 = v1.replace(',','#')
    v3 = v2.replace('.','&')
    v4 = v3.replace('#','.')
    v5 = v4.replace('&',',')
    return v5

def format_german(value):
    v1 = f'{value:,.2f} €'
    v2 = v1.replace(',','#')
    v3 = v2.replace('.','%')
    v4 = v3.replace('#','.')
    v5 = v4.replace('%',',')
    return v5


st.sidebar.header('DEMAK Dashboard `Version 2`')
st.sidebar.title('Simulationsparameter')


uploaded_file = st.sidebar.file_uploader("Parameter Hochladen", type=["json"])

if uploaded_file:
    # Reading the uploaded JSON file
    uploaded_data = json.load(uploaded_file)

    # Update the values from the uploaded data
    #arbeitnehmer_anzahl = uploaded_data.get('Arbeitnehmeranzahl', arbeitnehmer_anzahl)
    #zins_zusage = uploaded_data.get('Zins Zusage', zins_zusage)


if uploaded_file:
    arbeitnehmer_anzahl = st.sidebar.number_input('Arbeitnehmeranzahl (AN)',min_value=0,value= uploaded_data.get('Arbeitnehmeranzahl'))
    zins_zusage = (st.sidebar.number_input('Zins Zusage (%)',min_value=0.0,value= uploaded_data.get('Zins Zusage') )/100)
    an_fin_jaehrlich_pro_an = st.sidebar.number_input('AN finanziert jährlich pro AN (€)',min_value=0.0,value=uploaded_data.get('an_fin_jaehrlich_pro_an'))
    ag_fin_jaehrlich_pro_an = st.sidebar.number_input('AG finanziert jährlich pro AN (€)',min_value=0.0,value=uploaded_data.get('ag_fin_jaehrlich_pro_an'))
    laufzeit = st.sidebar.number_input('Laufzeit Zusage (Jahre)',min_value=0,value=uploaded_data.get('laufzeit'))
    darlehenszins = (st.sidebar.number_input('Darlehenszins (%)',min_value=0.0,value=uploaded_data.get('darlehenszins'))/100)
    psv_beitragssatz = (st.sidebar.number_input('PSV-Beitragssatz (%)',min_value=0.0,value=uploaded_data.get('psv_beitragssatz'))/100)
    uk_verwaltung_jaehrlich_pro_an = st.sidebar.number_input('UK Verwaltung jährlich pro AN',min_value=0,value=uploaded_data.get('uk_verwaltung_jaehrlich_pro_an'))
    uk_verwaltung_einmalig_im_ersten_jahr = (st.sidebar.number_input('UK Verwaltung einmalig im ersten Jahr (%)',min_value=0.0,value=uploaded_data.get('uk_verwaltung_einmalig_im_ersten_jahr'))/100)
    p1_anlage_liq = (st.sidebar.number_input('Anlage Liquidität (%)',min_value=0.0,value=uploaded_data.get('p1_anlage_liq'))/100)

else:
    arbeitnehmer_anzahl = st.sidebar.number_input('Arbeitnehmeranzahl (AN)',min_value=0,value=100)
    zins_zusage = (st.sidebar.number_input('Zins Zusage (%)',min_value=0.0,value=3.00)/100)
    an_fin_jaehrlich_pro_an = st.sidebar.number_input('AN finanziert jährlich pro AN (€)',min_value=0.0,value=1200.0)
    ag_fin_jaehrlich_pro_an = st.sidebar.number_input('AG finanziert jährlich pro AN (€)',min_value=0.0,value=360.0)
    laufzeit = st.sidebar.number_input('Laufzeit Zusage (Jahre)',min_value=0,value=30)
    darlehenszins = (st.sidebar.number_input('Darlehenszins (%)',min_value=0.0,value=7.50)/100)
    psv_beitragssatz = (st.sidebar.number_input('PSV-Beitragssatz (%)',min_value=0.0,value=0.25)/100)
    uk_verwaltung_jaehrlich_pro_an = st.sidebar.number_input('UK Verwaltung jährlich pro AN',min_value=0,value=89)
    uk_verwaltung_einmalig_im_ersten_jahr = (st.sidebar.number_input('UK Verwaltung einmalig im ersten Jahr (%)',min_value=0.0,value=2.00)/100)
    p1_anlage_liq = (st.sidebar.number_input('Anlage Liquidität (%)',min_value=0.0,value=0.0)/100)

steuern_UK = 0.1583 #(st.sidebar.number_input('Steuern UK (e.V.) (%)',min_value=0.0,value=15.83)/100)
steuer_ersparnis = 0.3 #(st.sidebar.number_input('Steuerersparnis (%)',min_value=0.0,value=30.00)/100)
passiva_2 = 0


st.sidebar.title('Eröffnungsbilanz')
col3, col4 = st.sidebar.columns(2)
col3.subheader('Aktiva')
col4.subheader('Passiva')

if uploaded_file:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        anlagevermoegen = st.number_input('Anlagevermögen',min_value=0,value=uploaded_data.get('Anlagevermögen'))
        umlaufvermögen = st.number_input('Umlaufvermögen',min_value=0,value=0, disabled=True)
        vorraete = st.number_input('Vorräte',min_value=0,value=uploaded_data.get('Vorräte'))
        kurzfristige_forderungen = st.number_input('Kurzfristige Forderungen',min_value=0,value=uploaded_data.get('Kurzfristige Forderungen'))
        zahlungsmittel = st.number_input('Zahlungsmittel',min_value=0,value=uploaded_data.get('Zahlungsmittel'))
    with col2:
        eigenkapital = st.number_input('Eigenkapital',min_value=0,value=0, disabled=True)
        fremdkapital = st.number_input('Fremdkapital',min_value=0,value=0, disabled=True)
        fk_kurzfristig = st.number_input('kurzfristig (FK kurzfr.)',min_value=0,value=uploaded_data.get('kurzfristig (FK kurzfr.)'))
        fk_langfristig = st.number_input('langfristig (FK langfr.)',min_value=0,value=uploaded_data.get('langfristig (FK langfr.)'))
else:
    col1, col2 = st.sidebar.columns(2)
    with col1:
        anlagevermoegen = st.number_input('Anlagevermögen',min_value=0,value=0)
        umlaufvermögen = st.number_input('Umlaufvermögen',min_value=0,value=0, disabled=True)
        vorraete = st.number_input('Vorräte',min_value=0,value=0)
        kurzfristige_forderungen = st.number_input('Kurzfristige Forderungen',min_value=0,value=0)
        zahlungsmittel = st.number_input('Zahlungsmittel',min_value=0,value=0)
    with col2:
        eigenkapital = st.number_input('Eigenkapital',min_value=0,value=0, disabled=True)
        fremdkapital = st.number_input('Fremdkapital',min_value=0,value=0, disabled=True)
        fk_kurzfristig = st.number_input('kurzfristig (FK kurzfr.)',min_value=0,value=0)
        fk_langfristig = st.number_input('langfristig (FK langfr.)',min_value=0,value=0)

# Create options from 1 to x
default_index = 0
options = list(range(1, laufzeit + 2))
st.sidebar.title('Musterbilanz')
# Create a selectbox with the options

c1, c2 = st.sidebar.columns(2)
with c1:
    bilanz_nach_jahren = st.selectbox('Bilanz nach X Jahren:', options, index=default_index)
    zusaetzliche_dotierung_j_n = st.selectbox('Zusätzlich Dotierung:', ('nein', 'ja'))
with c2:
    bilanzverlaengerung_j_n = st.selectbox('Bilanzverlängerung:', ('ja', 'nein'))

# Define flags for each metric's visibility
st.sidebar.title('Finanzwirtschaftliche Bilanzkennzahlen')
d1, d2 = st.sidebar.columns(2)
with d1:
    show_eigenkapital_quote = st.checkbox("Eigenkapitalquote", value=True)
    show_anspannungsgrad = st.checkbox("Anspannungsgrad", value=True)
    show_statischer_verschuldungsgrad = st.checkbox("Statischer Verschuldungsgrad", value=True)
    show_intensitaet_langfristiges_kapital = st.checkbox("Intensität langfristigen Kapitals", value=True)
    show_liquiditaet_1_grades = st.checkbox("Liquidität 1. Grades", value=True)
with d2:
    show_liquiditaet_2_grades = st.checkbox("Liquidität 2. Grades", value=True)
    show_liquiditaet_3_grades = st.checkbox("Liquidität 3. Grades", value=True)
    show_net_working_capital = st.checkbox("Net Working Capital", value=True)
    show_deckungsgrad_a = st.checkbox("Deckungsgrad A", value=True)
    show_deckungsgrad_b = st.checkbox("Deckungsgrad B", value=True)

# Add a button to trigger the save
st.sidebar.title(' ')
if st.sidebar.button('Parameter Speichern'):
    # Creating a dictionary of parameters to save
    data_to_save = {
        'Arbeitnehmeranzahl': arbeitnehmer_anzahl,
        'Zins Zusage': zins_zusage*100,
        'an_fin_jaehrlich_pro_an': an_fin_jaehrlich_pro_an,
        'ag_fin_jaehrlich_pro_an': ag_fin_jaehrlich_pro_an,
        'laufzeit': laufzeit,
        'darlehenszins': darlehenszins*100,
        'psv_beitragssatz': psv_beitragssatz*100,
        'uk_verwaltung_jaehrlich_pro_an': uk_verwaltung_jaehrlich_pro_an,
        'uk_verwaltung_einmalig_im_ersten_jahr': uk_verwaltung_einmalig_im_ersten_jahr*100,
        'p1_anlage_liq': p1_anlage_liq*100,
        'Anlagevermögen': anlagevermoegen,
        'Vorräte': vorraete,
        'Kurzfristige Forderungen': kurzfristige_forderungen,
        'Zahlungsmittel': zahlungsmittel,
        'kurzfristig (FK kurzfr.)': fk_kurzfristig,
        'langfristig (FK langfr.)': fk_langfristig
    }

    # Convert dictionary to JSON string
    json_str = json.dumps(data_to_save, indent=4)

    # Convert the string to bytes
    b64 = base64.b64encode(json_str.encode()).decode()

    # Provide a link to download the JSON file
    href = f'<a href="data:file/json;base64,{b64}" download="parameters.json">Parameter Herunterladen</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)





#Balance sheet calculations
umlaufvermögen = vorraete+kurzfristige_forderungen+zahlungsmittel
gesamtkapital_aktiva = anlagevermoegen + umlaufvermögen
fremdkapital = fk_kurzfristig + fk_langfristig
eigenkapital = gesamtkapital_aktiva - fremdkapital
gesamtkapital_passiva = eigenkapital + fremdkapital

# Create Dataframe
df = pd.DataFrame()
an_finanziert_jaehrlich_gesamt = arbeitnehmer_anzahl * an_fin_jaehrlich_pro_an
ag_finanziert_jaehrlich_gesamt = arbeitnehmer_anzahl * ag_fin_jaehrlich_pro_an
an_ag_finanziert_jaehrlich_gesamt = an_finanziert_jaehrlich_gesamt+ag_finanziert_jaehrlich_gesamt
kapital_bei_ablauf = (pow((1+zins_zusage),laufzeit)-1)/zins_zusage*(1+zins_zusage)*an_ag_finanziert_jaehrlich_gesamt
davon_an = (kapital_bei_ablauf/an_ag_finanziert_jaehrlich_gesamt)*an_finanziert_jaehrlich_gesamt

#Initialize Columns:
df['Jahr'] = range(1, laufzeit +2)

# initialize fields
df['Zulässiges Kassenvemögen'] = 0 #B
df['Höchstzulässiges Kassenvermögen'] = 0 #C
df['Zulässige Dotierung'] = 0 #D
df['Überdotierung'] = 0 #E
df['Darlehenszinsen'] = 0 #F
df['Zinsanteil Überdotierung'] = 0 #G
df['Steuern UK (e.V.)'] = 0 #H
df['Versorgung fällig'] = 0 #I
df['Darlehensänderung'] = 0 #J
df['Tatsächliches Kassenvermögen'] = 100 #K
df['Kosten UK-Verwaltung'] = 0 #L
df['PSV Beitrag'] = 0 #M
df['EU + SV Ersparnis'] = 0 #N
df['Steuerersparnis'] = 0 #O
df['Liquiditätsänderung'] = 0 #P
df['Anlage Liquidität'] = 0 #Q
df['Barwert Versorgung'] = 0 #T


# Main loop
for i in range(laufzeit+1):
    if i == 0:
        df.loc[i, 'Zulässiges Kassenvemögen'] = (kapital_bei_ablauf / 10) * 0.25 * 8 #B
        df.loc[i, 'Höchstzulässiges Kassenvermögen'] = df.loc[i, 'Zulässiges Kassenvemögen']*1.25 #C
        df.loc[i, 'Zulässige Dotierung'] = (kapital_bei_ablauf/10*0.25)
        df.loc[i, 'Tatsächliches Kassenvermögen'] =df.loc[i, 'Zulässige Dotierung']
        df.loc[i, 'PSV Beitrag'] = (davon_an/10)*0.25*20*psv_beitragssatz #M
        df.loc[i, 'Kosten UK-Verwaltung'] = (kapital_bei_ablauf*uk_verwaltung_einmalig_im_ersten_jahr)+(arbeitnehmer_anzahl*uk_verwaltung_jaehrlich_pro_an)
        df.loc[i, 'EU + SV Ersparnis'] = an_finanziert_jaehrlich_gesamt*1.2
        df.loc[i, 'Steuerersparnis'] = (df.loc[i, 'EU + SV Ersparnis']-df.loc[i,'PSV Beitrag']-df.loc[i,'Kosten UK-Verwaltung']-df.loc[i,'Zulässige Dotierung'])*steuer_ersparnis*-1
        df.loc[i, 'Liquiditätsänderung'] = df.loc[i, 'EU + SV Ersparnis']+ df.loc[i,'Steuerersparnis']-df.loc[i, 'PSV Beitrag']-df.loc[i, 'Kosten UK-Verwaltung']
        df.loc[i, 'Anlage Liquidität'] = df.loc[i, 'Liquiditätsänderung']
        df.loc[i, 'Barwert Versorgung'] = 0
        pass

    elif i == (laufzeit):
        df.loc[i, 'Zulässiges Kassenvemögen'] = 0
        df.loc[i, 'Höchstzulässiges Kassenvermögen'] = 0
        #df.loc[i, 'Zulässige Dotierung'] = 0
        df.loc[i, 'Versorgung fällig'] = kapital_bei_ablauf
        df['Darlehenszinsen'] = df['Tatsächliches Kassenvermögen'].shift(fill_value=0) * darlehenszins #F ###Check
        #df.loc[i,'Darlehensänderung'] = df.loc[i,'Zulässige Dotierung'] + df.loc[i,'Darlehenszinsen'] - df.loc[i, 'Steuern UK (e.V.)']#.shift(fill_value=0) #J ##ÄNDERUNG


        if zusaetzliche_dotierung_j_n == 'nein': ##ÄNDERUNG
            df.loc[i,'Darlehensänderung'] = df.loc[i-1, 'Tatsächliches Kassenvermögen']*-1 ##ÄNDERUNG


        #df.loc[i,'Tatsächliches Kassenvermögen'] = df.loc[i-1,'Tatsächliches Kassenvermögen'] + df.loc[i,'Darlehensänderung'] - df.loc[i,'Versorgung fällig'] #K
        df.loc[i,'Tatsächliches Kassenvermögen'] = 0 ##ÄNDERUNG
        df['Überdotierung'] = df['Tatsächliches Kassenvermögen'] - df['Höchstzulässiges Kassenvermögen'] #E

        if df.loc[i-1, 'Überdotierung'] > 0:
            df.loc[i, 'Zinsanteil Überdotierung'] = (df.loc[i-1, 'Überdotierung'] / df.loc[i-1, 'Tatsächliches Kassenvermögen']) * df.loc[i-1, 'Darlehenszinsen'] #G
        else:
            df.loc[i, 'Zinsanteil Überdotierung'] = 0 ##ÄNDERUNG
        df.loc[i, 'Steuern UK (e.V.)'] = (df.loc[i, 'Zinsanteil Überdotierung']*steuern_UK)
        df.loc[i, 'Zulässige Dotierung'] = kapital_bei_ablauf - df.loc[i-1,'Tatsächliches Kassenvermögen'] - df.loc[i, 'Darlehenszinsen'] + df.loc[i, 'Steuern UK (e.V.)'] #ÄNDERUNG, zeile neu hinzugefügt

        if zusaetzliche_dotierung_j_n == 'ja': ##ÄNDERUNG
            df.loc[i,'Darlehensänderung'] = df.loc[i, 'Zulässige Dotierung'] + df.loc[i, 'Darlehenszinsen'] - df.loc[i, 'Steuern UK (e.V.)'] - df.loc[i, 'Versorgung fällig']  #J ###ÄNDERUNG

        df.loc[df['Überdotierung'] > 0, 'Steuern UK (e.V.)'] = (df['Zinsanteil Überdotierung']*steuern_UK) #H
        df.loc[i, 'EU + SV Ersparnis'] = 0
        #df.loc[i, 'Steuerersparnis'] = (-df.loc[i, 'Darlehenszinsen'])*steuer_ersparnis*-1 #O

        df.loc[i, 'Kosten UK-Verwaltung'] = arbeitnehmer_anzahl*uk_verwaltung_jaehrlich_pro_an
        df.loc[i, 'PSV Beitrag'] = (kapital_bei_ablauf/10)*0.25*20*psv_beitragssatz
        df['Steuerersparnis'] = (df['EU + SV Ersparnis']-df['PSV Beitrag']-df[ 'Kosten UK-Verwaltung']-df['Darlehenszinsen']-df['Zulässige Dotierung'])*steuer_ersparnis*-1 #O
        df['Liquiditätsänderung'] = df['EU + SV Ersparnis']+df['Steuerersparnis']-df['PSV Beitrag']-df['Kosten UK-Verwaltung']-df['Steuern UK (e.V.)']-df['Versorgung fällig']
        df.loc[i, 'Anlage Liquidität'] = df.loc[i-1, 'Anlage Liquidität']*(1+p1_anlage_liq)+df.loc[i, 'Liquiditätsänderung']
        df.loc[i, 'Barwert Versorgung'] = df.loc[i-1, 'Barwert Versorgung']*(1+zins_zusage)+an_ag_finanziert_jaehrlich_gesamt*(1+zins_zusage)
        pass

    #elif i == (laufzeit+1):
        #df.loc[i, 'Zulässiges Kassenvemögen'] = 0
        #df.loc[i, 'Höchstzulässiges Kassenvermögen'] = 0
        #df.loc[i, 'Versorgung fällig'] = 0
        #df['Darlehenszinsen'] = df['Tatsächliches Kassenvermögen'].shift(fill_value=0) * darlehenszins
        #if df.loc[i-1, 'Überdotierung'] > 0:
        #    df.loc[i, 'Zinsanteil Überdotierung'] = (df.loc[i-1, 'Überdotierung'] / df.loc[i-1, 'Tatsächliches Kassenvermögen']) * df.loc[i-1, 'Darlehenszinsen'] #G
        #else:
        #    df.loc[i, 'Zinsanteil Überdotierung'] = 0 ##ÄNDERUNG
        #df.loc[i, 'Steuern UK (e.V.)'] = (df.loc[i, 'Zinsanteil Überdotierung']*steuern_UK)
        #df.loc[i,'Darlehensänderung'] = 0
        #df.loc[i,'Darlehensänderung'] = df.loc[i,'Darlehenszinsen'] - df.loc[i-1, 'Steuern UK (e.V.)'] - df.loc[i, 'Steuern UK (e.V.)']
        #df.loc[i,'Tatsächliches Kassenvermögen'] = df.loc[i-1,'Tatsächliches Kassenvermögen'] + df.loc[i,'Darlehensänderung'] - df.loc[i,'Versorgung fällig'] #K
        #df['Überdotierung'] = df['Tatsächliches Kassenvermögen'] - df['Höchstzulässiges Kassenvermögen'] #E
        #df.loc[i, 'EU + SV Ersparnis'] = 0
        #df.loc[i, 'Steuerersparnis'] = df.loc[i, 'Tatsächliches Kassenvermögen']*steuer_ersparnis*-1 #O
        #df['Steuerersparnis'] = (df['EU + SV Ersparnis']-df['PSV Beitrag']-df[ 'Kosten UK-Verwaltung']-df['Darlehenszinsen']-df['Zulässige Dotierung'])*steuer_ersparnis*-1 #O ###ANGEPASST
        #df.loc[i, 'Liquiditätsänderung'] = (df.loc[i,'Tatsächliches Kassenvermögen']*steuer_ersparnis)*-1- df.loc[i-1, 'Steuern UK (e.V.)'] - df.loc[i, 'Steuern UK (e.V.)']
        #df.loc[i, 'Anlage Liquidität'] = df.loc[i-1, 'Anlage Liquidität']*(1+p1_anlage_liq)+df.loc[i, 'Liquiditätsänderung']
        #df.loc[i, 'Barwert Versorgung'] = 0

    else:
        # calculations for subsequent years

        df.loc[i, 'Zulässiges Kassenvemögen'] = (kapital_bei_ablauf / 10) * 0.25 * 8 #B
        df.loc[i, 'Höchstzulässiges Kassenvermögen'] = df.loc[i, 'Zulässiges Kassenvemögen']*1.25 #C

        if i > 2:
            df.loc[i, 'PSV Beitrag'] = (kapital_bei_ablauf/10)*0.25*20*psv_beitragssatz
        else:
            df.loc[i, 'PSV Beitrag'] = (davon_an/10)*0.25*20*psv_beitragssatz  #M

        df['Darlehenszinsen'] = df['Tatsächliches Kassenvermögen'].shift(fill_value=0) * darlehenszins #F ###Check
        df.loc[i, 'Versorgung fällig'] = 0 #I

        if (df.loc[i-1, 'Tatsächliches Kassenvermögen']+df.loc[i, 'Darlehenszinsen']+(kapital_bei_ablauf/10)*0.25) <= df.loc[i, 'Zulässiges Kassenvemögen']:
            df.loc[i,'Zulässige Dotierung'] = (kapital_bei_ablauf/10)*0.25
        elif ((df.loc[i-1, 'Tatsächliches Kassenvermögen']+df.loc[i, 'Darlehenszinsen']+(kapital_bei_ablauf/10)*0.25) > df.loc[i, 'Zulässiges Kassenvemögen']):
            if (df.loc[i, 'Zulässiges Kassenvemögen'] - df.loc[i-1, 'Tatsächliches Kassenvermögen'] - df.loc[i, 'Darlehenszinsen'])>0:
                df.loc[i,'Zulässige Dotierung'] = df.loc[i, 'Zulässiges Kassenvemögen'] - df.loc[i-1, 'Tatsächliches Kassenvermögen'] - df.loc[i, 'Darlehenszinsen']
            else:
                df.loc[i,'Zulässige Dotierung'] = 0
        else:
            df.loc[i,'Zulässige Dotierung'] = 0


        if df.loc[i-1, 'Überdotierung'] > 0:
            df.loc[i, 'Zinsanteil Überdotierung'] = (df.loc[i-1, 'Überdotierung'] / df.loc[i-1, 'Tatsächliches Kassenvermögen']) * df.loc[i-1, 'Darlehenszinsen'] #G
        else:
            df.loc[i, 'Zinsanteil Überdotierung'] = 0 ##ÄNDERUNG

        df.loc[df['Überdotierung'] > 0, 'Steuern UK (e.V.)'] = (df['Zinsanteil Überdotierung']*steuern_UK) #H

        df['Darlehensänderung'] = df['Zulässige Dotierung'] + df['Darlehenszinsen'] - df['Steuern UK (e.V.)'] #J ###ÄNDERUNG
        df.loc[i,'Tatsächliches Kassenvermögen'] = df.loc[i-1,'Tatsächliches Kassenvermögen'] + df.loc[i,'Darlehensänderung'] - df.loc[i,'Versorgung fällig'] #K
        df['Überdotierung'] = df['Tatsächliches Kassenvermögen'] - df['Höchstzulässiges Kassenvermögen'] #E


        df.loc[i, 'Kosten UK-Verwaltung'] = arbeitnehmer_anzahl*uk_verwaltung_jaehrlich_pro_an #L
        df['EU + SV Ersparnis'] = an_finanziert_jaehrlich_gesamt*1.2 #N
        df['Steuerersparnis'] = (df['EU + SV Ersparnis']-df['PSV Beitrag']-df[ 'Kosten UK-Verwaltung']-df['Darlehenszinsen']-df['Zulässige Dotierung'])*steuer_ersparnis*-1 #O
        df['Liquiditätsänderung'] = df['EU + SV Ersparnis']+df['Steuerersparnis']-df['PSV Beitrag']-df['Kosten UK-Verwaltung']-df['Steuern UK (e.V.)'] #P #Check if we have to make a different case for row 1
        df.loc[i, 'Anlage Liquidität'] = df.loc[i-1, 'Anlage Liquidität']*(1+p1_anlage_liq)+df.loc[i, 'Liquiditätsänderung'] #Q

        if i == 1:
            df.loc[i, 'Barwert Versorgung'] = an_ag_finanziert_jaehrlich_gesamt*(1+zins_zusage)
        else: df.loc[i, 'Barwert Versorgung'] = df.loc[i-1, 'Barwert Versorgung']*(1+zins_zusage)+an_ag_finanziert_jaehrlich_gesamt*(1+zins_zusage)


#Logo
logo_path = "ressources/demak.png"  # Adjust the path to your logo file
logo = Image.open(logo_path)
new_size = (int(logo.width * 1), int(logo.height * 1))
resized_logo = logo.resize(new_size)
st.image(resized_logo)

# Row A1
st.title('KPIs')
col1, col2, col3, col4 = st.columns(4)
col1.metric("AN finanziert jährlich gesamt",format_german(an_finanziert_jaehrlich_gesamt))
col2.metric("AG finanziert jährlich gesamt",format_german(ag_finanziert_jaehrlich_gesamt))
col3.metric("AN + AG finanziert jährlich gesamt",format_german(an_ag_finanziert_jaehrlich_gesamt))
col4.metric("Kapital bei Ablauf",format_german(kapital_bei_ablauf))
#col5.metric("Humidity", str(zins_zusage)+"%", "4%")

#Row A2
col1, col2, col3, col4 = st.columns(4)
col4.metric("davon AN",format_german(davon_an))

# Display the DataFrame as a table in Streamlit
df = df.round(2)
st.dataframe(df)

csv = df.to_csv(index=False)
st.download_button(
    label="Als CSV herunterladen",
    data=csv,
    file_name="data.csv",
    mime="text/csv",
)

#Header
st.title("   ")
st.title("Eröffnungsbilanz")
aktiva, passiva = st.columns(2)
with aktiva:
    st.header("Aktiva")
with passiva:
    st.header("Passiva")

st.markdown('<hr style="border:1px solid black">', unsafe_allow_html=True)

#Sheet
aktiva_label, aktiva_value, passiva_label, passiva_value = st.columns(4)

with aktiva_label:
    st.subheader("1 Anlagevermögen")
    st.subheader("2 Umlaufvermögen")
    st.subheader("2.1 Vorräte")
    st.subheader("2.2 kurzfristige Forderungen")
    st.subheader("2.3 Zahlungsmittel")
with aktiva_value:
    st.subheader(format_german(anlagevermoegen))
    st.subheader(format_german(umlaufvermögen))
    st.subheader(format_german(vorraete))
    st.subheader(format_german(kurzfristige_forderungen))
    st.subheader(format_german(zahlungsmittel))
with passiva_label:
    st.subheader("1 Eigenkapital")
    st.subheader("2 Fremdkapital")
    st.subheader("2.1 kurzfristig (FK kurzfr.)")
    st.subheader("2.2 langfristig (FK langfr.)")
with passiva_value:
    st.subheader(format_german(eigenkapital))
    st.subheader(format_german(fremdkapital))
    st.subheader(format_german(fk_kurzfristig))
    st.subheader(format_german(fk_langfristig))

st.markdown('<hr style="border:1px solid black">', unsafe_allow_html=True)

# Create two columns for balance sheet
gk_aktiva_label, gk_aktiva_value, gk_passiva_label, gk_passiva_value = st.columns(4)
with gk_aktiva_label:
    st.subheader("Gesamtkapital Aktiva")
with gk_aktiva_value:
    formatted = gesamtkapital_aktiva #locale.format_string("%d", gesamtkapital_aktiva, grouping=True)
    st.subheader(format_german(gesamtkapital_aktiva)) #st.subheader(format_german())
with gk_passiva_label:
    st.subheader("Gesamtkapital Passiva")
with gk_passiva_value:
    formatted = gesamtkapital_passiva #locale.format_string("%d", gesamtkapital_passiva, grouping=True)
    st.subheader(format_german(gesamtkapital_passiva))

#avoid dividing by 0 denominator
def safe_division(numerator, denominator):
    if denominator == 0:
        return 0 # Or whatever value makes sense in this context
    else:
        return numerator / denominator
#Finanzwirtschaftliche Bilanzkennzahlen
eigenkapital_quote_1 = safe_division(eigenkapital,gesamtkapital_passiva)
anspannungsgrad_1 = safe_division(fremdkapital,gesamtkapital_passiva)
statischer_verschuldungsgrad_1 = safe_division(fremdkapital,eigenkapital)
intensitaet_langfristiges_kapital_1 = safe_division((eigenkapital+fk_langfristig),gesamtkapital_passiva)
liquiditaet_1_grades_1 = safe_division(zahlungsmittel,fk_kurzfristig)
liquiditaet_2_grades_1 = safe_division((zahlungsmittel+kurzfristige_forderungen),fk_kurzfristig)
liquiditaet_3_grades_1 = safe_division((zahlungsmittel+kurzfristige_forderungen+vorraete),fk_kurzfristig)
net_working_capital_1 = umlaufvermögen-fk_kurzfristig
deckungsgrad_a_1 = safe_division(eigenkapital,anlagevermoegen)
deckungsgrad_b_1 = safe_division((eigenkapital+fk_langfristig),anlagevermoegen)

st.title("   ")
st.title("Finanzwirtschaftliche Bilanzkennzahlen")
col1, col2, col3, col4, col5 = st.columns(5)


if show_eigenkapital_quote:
    col1.metric("Eigenkapitalquote", to_percentage(eigenkapital_quote_1))
if show_liquiditaet_2_grades:
    col1.metric("Liquidität 2. Grades", to_percentage(liquiditaet_2_grades_1))
if show_anspannungsgrad:
    col2.metric("Anspannungsgrad", to_percentage(anspannungsgrad_1))
if show_liquiditaet_3_grades:
    col2.metric("Liquidität 3. Grades", to_percentage(liquiditaet_3_grades_1))
if show_statischer_verschuldungsgrad:
    col3.metric("Statischer Verschuldungsgrad", to_percentage(statischer_verschuldungsgrad_1))
if show_net_working_capital:
    col3.metric("Net Working Capital", format_german(net_working_capital_1))
if show_intensitaet_langfristiges_kapital:
    col4.metric("Intensität langfristigen Kapitals", to_percentage(intensitaet_langfristiges_kapital_1))
if show_deckungsgrad_a:
    col4.metric("Deckungsgrad A", to_percentage(deckungsgrad_a_1))
if show_liquiditaet_1_grades:
    col5.metric("Liquidität 1. Grades", to_percentage(liquiditaet_1_grades_1))
if show_deckungsgrad_b:
    col5.metric("Deckungsgrad B", to_percentage(deckungsgrad_b_1))


if bilanzverlaengerung_j_n == 'ja':
    bilanzverlängerung_txt = 'bei'
elif bilanzverlaengerung_j_n == 'nein':
    bilanzverlängerung_txt = 'ohne'
else:
    bilanzverlängerung_txt = 'error'

#Header
st.title("   ")
st.title("Musterbilanz nach "+ f"{bilanz_nach_jahren} Jahren und Liquiditätsanlage "+ f"{to_percentage(p1_anlage_liq)} "+ f"{bilanzverlängerung_txt} Bilanzverlängerung ")

aktiva, passiva = st.columns(2)
with aktiva:
    st.header("Aktiva")
with passiva:
    st.header("Passiva")

st.markdown('<hr style="border:1px solid black">', unsafe_allow_html=True)

#Sheet
aktiva_label, aktiva_value, passiva_label, passiva_value = st.columns(4)

#Balance sheet calculations
anlagevermoegen_2 = anlagevermoegen
vorraete_2 = vorraete
kurzfristige_forderungen_2 = kurzfristige_forderungen

if bilanzverlaengerung_j_n == 'ja':
    if bilanz_nach_jahren == laufzeit+1:
        zahlungsmittel_2 = df.loc[bilanz_nach_jahren-1, 'Anlage Liquidität'] + zahlungsmittel
    else:
        zahlungsmittel_2 = df.loc[bilanz_nach_jahren, 'Anlage Liquidität'] + zahlungsmittel
elif bilanzverlaengerung_j_n == 'nein':
    zahlungsmittel_2 = zahlungsmittel
else:
    zahlungsmittel_2 = 0

##umlaufvermögen_2 = vorraete_2 + kurzfristige_forderungen_2 + zahlungsmittel_2
##gesamtkapital_aktiva_2 = anlagevermoegen + umlaufvermögen_2
##fk_kurzfristig_2 = fk_kurzfristig

if bilanzverlaengerung_j_n == 'ja':
    fk_kurzfristig_2 = fk_kurzfristig
elif bilanzverlaengerung_j_n == 'nein':
    if bilanz_nach_jahren == laufzeit+1:
        fk_kurzfristig_2 = fk_kurzfristig - df.loc[bilanz_nach_jahren-1, 'Anlage Liquidität']
        if fk_kurzfristig_2 < 0:
            zahlungsmittel_2 = zahlungsmittel_2 + abs(fk_kurzfristig_2)
            fk_kurzfristig_2 = 0
    else:
        fk_kurzfristig_2 = fk_kurzfristig - df.loc[bilanz_nach_jahren, 'Anlage Liquidität']
        if fk_kurzfristig_2 < 0:
            zahlungsmittel_2 = zahlungsmittel_2 + abs(fk_kurzfristig_2)
            fk_kurzfristig_2 = 0
else:
    fk_kurzfristig_2 = 0

if bilanz_nach_jahren == laufzeit+1:
    fk_langfristig_2 = fk_langfristig
else:
    fk_langfristig_2 = fk_langfristig + df.loc[bilanz_nach_jahren, 'Tatsächliches Kassenvermögen']
if bilanz_nach_jahren != laufzeit+1:
    if (df.loc[bilanz_nach_jahren-1, 'Barwert Versorgung']-df.loc[bilanz_nach_jahren-1, 'Tatsächliches Kassenvermögen'])>0:
        bilanzanhang_2 = df.loc[bilanz_nach_jahren, 'Barwert Versorgung']-df.loc[bilanz_nach_jahren, 'Tatsächliches Kassenvermögen']
    else:
        bilanzanhang_2 = 0
else:
    bilanzanhang_2 = 0

umlaufvermögen_2 = vorraete_2 + kurzfristige_forderungen_2 + zahlungsmittel_2
gesamtkapital_aktiva_2 = anlagevermoegen + umlaufvermögen_2
#fk_kurzfristig_2 = fk_kurzfristig

fremdkapital_2 = fk_kurzfristig_2 + fk_langfristig_2 #+ bilanzanhang_2
eigenkapital_2 = gesamtkapital_aktiva_2 - fremdkapital_2
gesamtkapital_passiva_2 = eigenkapital_2 + fremdkapital_2

with aktiva_label:
    st.subheader("1 Anlagevermögen")
    st.subheader("2 Umlaufvermögen")
    st.subheader("2.1 Vorräte")
    st.subheader("2.2 kurzfristige Forderungen")
    st.subheader("2.3 Zahlungsmittel")
with aktiva_value:
    st.subheader(format_german(anlagevermoegen_2))
    st.subheader(format_german(umlaufvermögen_2))
    st.subheader(format_german(vorraete_2))
    st.subheader(format_german(kurzfristige_forderungen_2))
    st.subheader(format_german(zahlungsmittel_2))
with passiva_label:
    st.subheader("1 Eigenkapital")
    st.subheader("2 Fremdkapital")
    st.subheader("2.1 kurzfristig (FK kurzfr.)")
    st.subheader("2.2 langfristig (FK langfr.)")
    #st.subheader("3 Bilanzanhang")
with passiva_value:
    st.subheader(format_german(eigenkapital_2))
    st.subheader(format_german(fremdkapital_2))
    st.subheader(format_german(fk_kurzfristig_2))
    st.subheader(format_german(fk_langfristig_2))
    #st.subheader(format_german(bilanzanhang_2))

st.markdown('<hr style="border:1px solid black">', unsafe_allow_html=True)

# Create two columns for balance sheet
gk_aktiva_label, gk_aktiva_value, gk_passiva_label, gk_passiva_value = st.columns(4)
with gk_aktiva_label:
    st.subheader("Gesamtkapital Aktiva")
with gk_aktiva_value:
    formatted = format_german(gesamtkapital_aktiva_2) #locale.format_string("%d", gesamtkapital_aktiva_2, grouping=True)
    st.subheader(format_german(gesamtkapital_aktiva_2))
    #st.subheader(f'{gesamtkapital_aktiva_2:,}'.replace(',','.'))
with gk_passiva_label:
    st.subheader("Gesamtkapital Passiva")
    st.subheader("_Bilanzanhang_")
with gk_passiva_value:
    formatted = gesamtkapital_passiva_2 #locale.format_string("%d", gesamtkapital_passiva_2, grouping=True)
    st.subheader(format_german(gesamtkapital_passiva_2))
    st.subheader(format_german(bilanzanhang_2))



#Finanzwirtschaftliche Bilanzkennzahlen
eigenkapital_quote_2 = safe_division(eigenkapital_2,gesamtkapital_passiva_2)
anspannungsgrad_2 = safe_division(fremdkapital_2,gesamtkapital_passiva_2)
statischer_verschuldungsgrad_2 = safe_division(fremdkapital_2,eigenkapital_2)
intensitaet_langfristiges_kapital_2 = safe_division((eigenkapital_2+fk_langfristig_2),gesamtkapital_passiva_2)
liquiditaet_1_grades_2 = safe_division(zahlungsmittel_2,fk_kurzfristig_2)
liquiditaet_2_grades_2 = safe_division((zahlungsmittel_2+kurzfristige_forderungen_2),fk_kurzfristig_2)
liquiditaet_3_grades_2 = safe_division((zahlungsmittel_2+kurzfristige_forderungen+vorraete_2),fk_kurzfristig_2)
net_working_capital_2 = umlaufvermögen_2-fk_kurzfristig_2
deckungsgrad_a_2 = safe_division(eigenkapital_2,anlagevermoegen_2)
deckungsgrad_b_2 = safe_division((eigenkapital_2+fk_langfristig_2),anlagevermoegen_2)

eigenkapital_quote_2_change = safe_division(eigenkapital_quote_2,eigenkapital_quote_1)-1
anspannungsgrad_2_change = safe_division(anspannungsgrad_2,anspannungsgrad_1)-1
statischer_verschuldungsgrad_2_change = safe_division(statischer_verschuldungsgrad_2,statischer_verschuldungsgrad_1)-1
intensitaet_langfristiges_kapital_2_change = safe_division(intensitaet_langfristiges_kapital_2,intensitaet_langfristiges_kapital_1)-1
liquiditaet_1_grades_2_change = safe_division(liquiditaet_1_grades_2,liquiditaet_1_grades_1)-1
liquiditaet_2_grades_2_change = safe_division(liquiditaet_2_grades_2,liquiditaet_2_grades_1)-1
liquiditaet_3_grades_2_change = safe_division(liquiditaet_3_grades_2,liquiditaet_3_grades_1)-1
net_working_capital_2_change = safe_division(net_working_capital_2,net_working_capital_1)-1
deckungsgrad_a_2_change = safe_division(deckungsgrad_a_2,deckungsgrad_a_1)-1
deckungsgrad_b_2_change = safe_division(deckungsgrad_b_2,deckungsgrad_b_1)-1

st.title("   ")
st.title("Finanzwirtschaftliche Bilanzkennzahlen")
col1, col2, col3, col4, col5 = st.columns(5)
if show_eigenkapital_quote:
    col1.metric("Eigenkapitalquote", to_percentage(eigenkapital_quote_2), to_percentage(eigenkapital_quote_2_change))
if show_liquiditaet_2_grades:
    col1.metric("Liquidität 2. Grades", to_percentage(liquiditaet_2_grades_2), to_percentage(liquiditaet_2_grades_2_change))
if show_anspannungsgrad:
    col2.metric("Anspannungsgrad", to_percentage(anspannungsgrad_2), to_percentage(anspannungsgrad_2_change))
if show_liquiditaet_3_grades:
    col2.metric("Liquidität 3. Grades", to_percentage(liquiditaet_3_grades_2), to_percentage(liquiditaet_3_grades_2_change))
if show_statischer_verschuldungsgrad:
    col3.metric("Statischer Verschuldungsgrad", to_percentage(statischer_verschuldungsgrad_2), to_percentage(statischer_verschuldungsgrad_2_change))
if show_net_working_capital:
    col3.metric("Net Working Capital", format_german(net_working_capital_2), to_percentage(net_working_capital_2_change))
if show_intensitaet_langfristiges_kapital:
    col4.metric("Intensität langfristigen Kapitals", to_percentage(intensitaet_langfristiges_kapital_2), to_percentage(intensitaet_langfristiges_kapital_2_change))
if show_deckungsgrad_a:
    col4.metric("Deckungsgrad A", to_percentage(deckungsgrad_a_2), to_percentage(deckungsgrad_a_2_change))
if show_liquiditaet_1_grades:
    col5.metric("Liquidität 1. Grades", to_percentage(liquiditaet_1_grades_2), to_percentage(liquiditaet_1_grades_2_change))
if show_deckungsgrad_b:
    col5.metric("Deckungsgrad B", to_percentage(deckungsgrad_b_2), to_percentage(deckungsgrad_b_2_change))

###Markdowns
st.markdown("""
<style>
div[data-testid="metric-container"] {
    background-color: #FFFFFF;
    border: 1px solid #CCCCCC;
    padding: 5% 5% 5% 10%;
    border-radius: 15px;
    border-left: 0.5rem solid #fdff00 !important;
    box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: black;
}
</style>
"""
            , unsafe_allow_html=True)

