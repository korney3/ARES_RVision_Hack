import requests
from flask import Flask, request, Response, jsonify
import numpy as np
import pandas as pd
from flask_cors import CORS
from requests import Request, Session
from werkzeug.utils import secure_filename
import os
import json
import re
import glob

app = Flask(__name__)
cors = CORS(app)

from collections import Counter

#Very long regular str
match_str = r'Comment Panda|PLA Unit 61398|Advanced Persistent Threat 1|Byzantine Candor|Group 3|TG-8223|Comment Group|Brown Fox|GIF89a|ShadyRAT|Shanghai Group|Covert Grove|C0d0so|APT19|APT 19|Sunshop Group|temp\.bottle|LadyBoyle|PLA Unit 61486|Group 36|APT-2|MSUpdater|4HCrew|SULPHUR|SearchFire|TG-6952|Gothic Panda|TG-0110|APT 3|Group 6|UPS Team|Buckeye|Boyusec|BORON|BRONZE MAYFAIR|DUBNIUM|Fallout Team|Karba|Luder|Nemim|Nemin|Tapaoux|Pioneer|Shadow Crane|APT-C-06|SIG25|TUNGSTEN BRIDGE|T-APT-02|Numbered Panda|TG-2754|BeeBus|Group 22|DynCalc|Calc Team|DNSCalc|Crimson Iron|APT12|APT 12|BRONZE GLOBE|APT16|SVCMONDR|APT 17|Deputy Dog|Group 8|APT17|Hidden Lynx|Tailgater Team|Dogfish|BRONZE KEYSTONE|Dynamite Panda|TG-0416|APT 18|SCANDIUM|PLA Navy|APT18|Winnti Umbrella|Winnti Group|Suckfly|APT41|APT 41|Group72|Group 72|Blackfly|LEAD|WICKED SPIDER|WICKED PANDA|BARIUM|BRONZE ATLAS|BRONZE EXPORT|Red Kelpie|Deep Panda|WebMasters|APT 19|KungFu Kittens|Black Vine|Group 13|PinkPanther|Sh3llCr3w|BRONZE FIRESTONE|PLA Unit 78020|APT 30|APT30|Override Panda|Camerashy|APT\.Naikon|Lotus Panda|Hellsing|BRONZE GENEVA|Spring Dragon|ST Group|Esile|DRAGONFISH|BRONZE ELGIN|Elise|Black Vine|TEMP\.Avengers|TG-3390|APT 27|TEMP\.Hippo|Group 35|Bronze Union|ZipToken|HIPPOTeam|APT27|Operation Iron Tiger|Iron Tiger APT|BRONZE UNION|Lucky Mouse|APT10|APT 10|MenuPass|Menupass Team|menuPass|menuPass Team|happyyongzi|POTASSIUM|DustStorm|Red Apollo|CVNX|HOGFISH|Cloud Hopper|BRONZE RIVERSIDE|APT 9|Flowerlady/Flowershow|Flowerlady|Flowershow|Goblin Panda|Conimes|Cycldek|Vixen Panda|Ke3Chang|GREF|Playful Dragon|APT 15|APT15|Metushy|Lurid|Social Network Team|Royal APT|BRONZE PALACE|APT14|APT 14|QAZTeam|ALUMINUM|APT 21|APT21|TravNet|IceFog|Dagger Panda|Trident|PittyTiger|MANGANESE|BRONZE WOODLAND|Rotten Tomato|Sneaky Panda|Elderwood|Elderwood Gang|SIG22|Shrouded Crossbow|PLA Navy|Wisp Team|APT20|APT 20|TH3Bug|Twivy|Admin338|Team338|MAGNESIUM|admin@338|APT23|APT 23|KeyBoy|TropicTrooper|Tropic Trooper|BRONZE HOBART|SaffronRose|Saffron Rose|AjaxSecurityTeam|Ajax Security Team|Group 26|Sayad|ITSecTeam|Threat Group 2889|TG-2889|Ghambar|Newscaster|Parastoo|iKittens|Group 83|Newsbeef|NewsBeef|APT 33|Elfin|MAGNALLIUM|Refined Kitten|HOLMIUM|COBALT TRINITY|Group 42|VOYEUR|TEMP\.Beanie|Operation Woolen Goldfish|Operation Woolen-Goldfish|Thamar Reservoir|Timberworm|Operation Cleaver|Tarh Andishan|Alibaba|2889|TG-2889|Cobalt Gypsy|Rocket_Kitten|Cutting Kitten|Group 41|Magic Hound|APT35|APT 35|TEMP\.Beanie|Ghambar|FallagaTeam|Vikingdom|APT 28|APT28|Pawn Storm|PawnStorm|Fancy Bear|Sednit|SNAKEMACKEREL|TsarTeam|Tsar Team|TG-4127|Group-4127|STRONTIUM|TAG_0700|Swallowtail|IRON TWILIGHT|Group 74|SIG40|Grizzly Steppe|apt_sofacy|Dukes|Group 100|Cozy Duke|CozyDuke|EuroAPT|CozyBear|CozyCar|Cozer|Office Monkeys|OfficeMonkeys|APT29|Cozy Bear|The Dukes|Minidionis|SeaDuke|Hammer Toss|YTTRIUM|Iron Hemlock|Grizzly Steppe|Turla|Snake|Venomous Bear|VENOMOUS Bear|Group 88|Waterbug|WRAITH|Turla Team|Uroburos|Pfinet|TAG_0530|KRYPTON|Hippo Team|Pacifier APT|Popeye|SIG23|Iron Hunter|MAKERSMARK|Dragonfly|Crouching Yeti|Group 24|Havex|CrouchingYeti|Koala Team|IRON LIBERTY|Sandworm Team|Black Energy|BlackEnergy|Quedagh|Voodoo Bear|TEMP\.Noble|Iron Viking|Sandworm|Carbanak|Carbon Spider|FIN7|GOLD NIAGARA|TeamSpy|Team Bear|Berserk Bear|Anger Bear|IRON LYRIC|FIN4|OperationTroy|Guardian of Peace|GOP|WHOis Team|Andariel|Subgroup: Andariel|Operation DarkSeoul|Dark Seoul|Hidden Cobra|Hastati Group|Andariel|Unit 121|Bureau 121|NewRomanic Cyber Army Team|Bluenoroff|Subgroup: Bluenoroff|Group 77|Labyrinth Chollima|Operation Troy|Operation GhostSecret|Operation AppleJeus|APT38|APT 38|Stardust Chollima|Whois Hacking Team|Zinc|Appleworm|Nickel Academy|APT-C-26|NICKEL GLADSTONE|COVELLITE|Appin|OperationHangover|DD4BC|Ambiorx|TunisianCyberArmy|Animal Farm|Snowglobe|SyrianElectronicArmy|SEA|C-Major|Transparent Tribe|Mythic Leopard|ProjectM|APT36|APT 36|TMP\.Lapis|Green Havildar|COPPER FIELDSTONE|FruityArmor|Chinastrats|Patchwork|Monsoon|Sarit|Quilted Tiger|APT-C-09|ZINC EMERSON|Moafee|BRONZE OVERBROOK|TG-3390|Emissary Panda|Strider|Sauron|Project Sauron|APT30|Skeleton Spider|ITG08|CorporacaoXRat|CorporationXRat|Twisted Kitten|Cobalt Gypsy|Crambus|Helix Kitten|APT 34|APT34|IRN2|Reuse team|Malware reusers|Dancing Salome|Lebanese Cedar|Reuse team|Dancing Salome|Gaza Hackers Team|Gaza cybergang|Gaza Cybergang|Operation Molerats|Extreme Jackal|Moonlight|ALUMINUM SARATOGA|StrongPity|Lion Soldiers Team|Phantom Turk|Crescent and Star|Turk Hack Team|Tilded Team|Lamberts|EQGRP|Longhorn|PLATINUM TERMINAL|Primitive Bear|Zhenbao|TEMP\.Zhenbao|Operation Mermaid|Prince of Persia|Cloudy Omega|Emdivi|Lamberts|the Lamberts|APT-C-39|OceanLotus Group|Ocean Lotus|OceanLotus|Cobalt Kitty|APT-C-00|SeaLotus|Sea Lotus|APT-32|APT 32|Ocean Buffalo|POND LOACH|TIN WOODLAWN|BISMUTH|Butterfly|Morpho|Sphinx Moth|TwoForOne|Sandworm|LeafMiner|Raspite|Machete|machete-apt|APT-C-43|Cobalt group|Cobalt Group|Cobalt gang|Cobalt Gang|GOLD KINGSWOOD|Cobalt Spider|CactusPete|Karma Panda|MANGANESE|BRONZE FLEETWOOD|APT22|BRONZE OLIVE|Bronze Butler|RedBaldKnight|APT26|Hippo Team|JerseyMikes|Turbine Panda|BRONZE EXPRESS|Superman|BRONZE WALKER|Slayer Kitten|PLA Navy|BRONZE EDISON|Sykipot|Velvet Chollima|Black Banshee|Thallium|Operation Stolen Pencil|The Mask|Mask|Ugly Face|Group 41|Islamic State Hacking Division|CCA|United Cyber Caliphate|UUC|CyberCaliphate|Fraternal Jackal|1\.php Group|APT6|Desert Falcon|Arid Viper|APT-C-23|Duqu Group|Skipper Turla|TEMP\.Zagros|Static Kitten|Seedworm|MERCURY|COBALT ULSTER|SixLittleMonkeys|APT 37|Group 123|Group123|ScarCruft|Reaper|Reaper Group|Red Eyes|Ricochet Chollima|Operation Daybreak|Operation Erebus|Venus 121|TEMP\.Periscope|TEMP\.Jumper|APT 40|APT40|BRONZE MOHAWK|GADOLINIUM|Kryptonite Panda|APT 34|APT 35|Newscaster Team|Palmetto Fusion|Allanite|OilRig|Greenbug|Dragonfly 2\.0|Dragonfly2|Berserker Bear|APT33|Emissary Panda|APT27|APT 27|Threat Group 3390|Bronze Union|Iron Tiger|TG-3390|TEMP\.Hippo|Group 35|ZipToken|Rancor group|Rancor|Rancor Group|Gorgon Group|Subaat|LazyMeerkat|DoNot Team|Donot Team|APT-C-35|BRONZE PRESIDENT|HoneyMyte|Red Lich|LOTUS PANDA|IAmTheKing|Iron Cyber Group|the Rocra|Cobalt Dickens|Roaming Mantis Group|The ShadowBrokers|TSB|Shadow Brokers|ShadowBrokers|Operation EvilTraffic|COBALT EDGEWATER|Golden Chickens|Golden Chickens01|Golden Chickens 01|Golden Chickens|Golden Chickens02|Golden Chickens 02|SectorJ04 Group|GRACEFUL SPIDER|GOLD TAHOE|GOLD ULRICK|TEMP\.MixMaster|TA542|Mummy Spider|GOLD CRESTWOOD|Nahr Elbard|Nahr el bared|Silence|Silence APT group|WHISPER SPIDER|APT 39|Chafer|REMIX KITTEN|COBALT HICKMAN|GOLD LOWELL|GOLD SWATHMORE|Blind Eagle|GoldMouse|COBALT DICKENS|Mabna Institute|TA407|APT 31|ZIRCONIUM|JUDGMENT PANDA|BRONZE VINEWOOD|Topgear|Comnie|BLACKGEAR|CIRCUIT PANDA|Temp\.Overboard|HUAPI|Snooping Dragon|Xenotime|COBALT LYCEUM|IMPERIAL KITTEN|Evil Eye|Calypso|Calypso APT|Golden Falcon|APT-C-27|RAZOR TIGER|Budminer cyberespionage group|Sapphire Mushroom|Blue Mushroom|NuclearCrisis|Empire Monkey|CobaltGoblin|GOLD ESSEX|badbullzvenom|DarkUniverse|SIG27|SIG37|APT-C-38 \(QiAnXin\)|SABER LION|TG-2884 \(SCWX CTU\)|Hive0081 \(IBM\)|SectorD01 \(NHSC\)|xHunt campaign \(Palo Alto\)|DeathStalker|PIONEER KITTEN|PARISITE|UNC757|TEMP\.Warlock|DarkHalo|APT3|APT2|APT 1|APT1|APT4|APT 4|APT 2|APT2'

def analyze_loc_document(path):
    
    """
    Parse document on local storage for threat_actor
    """
    
    with open(path) as f:
        lines = [line.rstrip('\n') for line in f if len(line)>2]
    
    treat_actors_list = [re.findall(re.compile(match_str), line) for line in lines if re.findall(re.compile(match_str), line)]
    
    treat_actors_list = sum(treat_actors_list, [])
    
    #If no threat_actors found
    if len(treat_actors_list)<1:
        return None, None, None, None, None, lines
    
    #main threat_actor can be observed more in document
    main, *secondary = [k for k,v in Counter(treat_actors_list).items()]
    
    #make a tag in the document
    lines = [re.sub('|'.join([main]+secondary), f'<THREAT_ACTOR>\g<0></THREAT_ACTOR>', line) for line in lines]
    
    #detect all possible synonyms for threat_actor
    actor_synonymous = {}
    for treat_actor_data in treat_actors['values']:
        try:
            if main in treat_actor_data['meta']['synonyms']:
                actor_synonymous[main] = treat_actor_data['meta']['synonyms']
                break
        except BaseException:
            continue
    
    #find techniques exploited by threat_actor
    group_techniques = []
    actor_found = False
    for group in caret_data['groups']:
        if main in group['aliases']:
            group_techniques.extend([i.replace('Technique/', '') for i in group['techniques']])
            actor_found = True

        if not actor_found:
            for alias in actor_synonymous[main]:
                if alias in group['aliases']:
                    group_techniques.extend([i.replace('Technique/', '') for i in group['techniques']])
                    actor_found = True
                if actor_found:
                    break
    
    return treat_actors_list, main, secondary, group_techniques, treat_actor_data, lines

@app.route('/analyze_document', methods=['POST'])
def analyze_document():
    
    """
    Parse document came from API for threat_actor
    """
    
    
    if request.method == 'POST':
        
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('.', filename))
        
        with open(os.path.join('.', filename)) as f:
            lines = [line.rstrip('\n') for line in f if len(line)>3]

        treat_actors_list = [re.findall(re.compile(match_str), line) for line in lines if re.findall(re.compile(match_str), line)]

        treat_actors_list = sum(treat_actors_list, [])
        
        #If no threat_actors found
        if len(treat_actors_list)<1:
   
            return jsonify({'treat_actors_list': None, 'main': None, 'secondary':None, 'group_techniques':None,
                'treat_actor_data':None, 'lines':lines})

        #main threat_actor can be observed more in document
        main, *secondary = [k for k,v in Counter(treat_actors_list).items()]
        
        #make a tag in the document
        lines = [re.sub('|'.join([main]+secondary), f'<THREAT_ACTOR>\g<0></THREAT_ACTOR>', line) for line in lines]
        
        #detect all possible synonyms for threat_actor
        actor_synonymous = {}
        for treat_actor_data in treat_actors['values']:
            try:
                if main in treat_actor_data['meta']['synonyms']:
                    actor_synonymous[main] = treat_actor_data['meta']['synonyms']
                    break
            except KeyError:
                continue

        #find techniques exploited by threat_actor
        group_techniques = []
        actor_found = False
        for group in caret_data['groups']:
            if main in group['aliases']:
                group_techniques.extend(group['techniques'])
                actor_found = True

            if not actor_found:
                for alias in actor_synonymous[main]:
                    if alias in group['aliases']:
                        group_techniques.extend(group['techniques'])
                        actor_found = True
                    if actor_found:
                        break
                        
        #Create links to attack.mitre for each technique
        techniques_link = []
        for i in group_techniques:
            try:
                techniques_link.append(f"https://attack.mitre.org/techniques/{i.replace('Technique/', '').split('.')[0]}/{i.replace('Technique/', '').split('.')[1]}")
            except IndexError:
                techniques_link.append(f"https://attack.mitre.org/techniques/{i.replace('Technique/', '')}/")

        group_techniques = [(i,j) for i,j in zip(group_techniques, techniques_link)]
 
        return jsonify({'treat_actors_list': treat_actors_list, 
                        'main': main, 
                        'secondary':secondary, 
                        'group_techniques':group_techniques,
                        'treat_actor_data':treat_actor_data, 
                        'lines':lines})

@app.route('/list_docs', methods=['GET'])
def available_docs():
    return jsonify({'available_docs': list(map(lambda x: x.replace('data/', ''), glob.glob('data/*.pdf.txt')))})
                    
@app.route('/analyze_local_doc', methods=['GET'])
def analyze_local_doc():
                    
    path = request.args.get('path', default='Operation_AppleJeus.pdf.txt', type=str)
    
    treat_actors_list, main, secondary, group_techniques, treat_actor_data, lines = analyze_loc_document(path=os.path.join('data', path))
    
    return jsonify({'treat_actors_list': treat_actors_list, 
                    'main': main, 
                    'secondary':secondary, 
                    'group_techniques':group_techniques,
                    'treat_actor_data':treat_actor_data, 
                    'lines':lines})

@app.route('/model_stats', methods=['GET'])
def model_stats():

    return jsonify({'known_treat_actors_for_3_years_data': 0.6436, 
                    'known_techniques': 0.923, 
                    'found techniques': 0.9081})
                    
    
@app.route('/potential_actors', methods=['GET'])
def define_actors():
    """
    Find actor by exploited technique
    """
    technique = request.args.get('technique', default='T1587.003', type=str)
    
    potential_actors = []
    for key in d:
        if technique in d[key]['techniques']:
            potential_actors.append(key)
            
    return jsonify({'potential_actors': potential_actors})
    
if __name__ == '__main__':
    
    #load Mitre and MISP json
    f = open('threat-actor.json',) 
    treat_actors = json.load(f) 
    f.close()

    f = open('caret-data.json',) 
    caret_data = json.load(f) 
    f.close()
    
    d = {}
    for doc in glob.glob('data/*'):
        treat_actors_list, main, secondary, group_techniques, treat_actor_data, lines = analyze_loc_document(doc)
        if main is not None:
            d[main] = {'docs':[], 'secondary_actors':[], 'techniques':[]}
            d[main]['docs'].append(doc)
            d[main]['secondary_actors'].extend(secondary)
            d[main]['techniques'].extend(group_techniques)
    
    app.run(host='0.0.0.0', port=5000)
