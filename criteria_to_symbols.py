from listen_ipa_dataset import CRITERIA_TAGS_ID


vowels_table = [[["i","i̹","y"], ["ɨ","ɨ̹","ʉ"], ["ɯ","u̜","u"]],
                [["ɪ","ɪ̹","ʏ"], ["ɪ̈","ɪ̹̈","ʏ̈"], ["ɯ̽","ʊ̜","ʊ"]],
                [["e","e̹","ø"], ["ɘ","ɘ̹","ɵ"], ["ɤ","o̜","o"]],
                [["e̞","e̹̞","ø̞"], ["ə̜","ə","ə̹"], ["ɤ̞","o̜̞","o̞"]],
                [["ɛ","ɛ̹","œ"], ["ɜ","ɜ̹","ɞ"], ["ʌ","ɔ̜","ɔ"]],
                [["æ","æ̹","œ̞"], ["æ̈","ɐ","ɐ̹"], ["ʌ̞","ɔ̜̞","ɔ̞"]],
                [["a","a̹","ɶ"], ["ä","ä̹","ɶ̈"], ["ɑ","ɒ̜","ɒ"]]]

MODS_TABLE_ADD = {"approx": "̞", "nasal": "̃", "plosive": "͐", "sibilant": "͒", "non-sib fr":"̐", "trill": "͙", "tap": "͓",
              "dental": "̪", "alveolar": "͇", "half_labialization": "̹", "retroflex": "˞"}
SUB_TABLE_ADD = {"lateral": "ˡ", "labialization": "ʷ", "bilabial": "ᵙ", "labiodental": "ᶹ", "palatal": "ʲ", "velar": "ˠ",
              "uvular": "ʶ", "pharyngeal": "ˤ", "glottal": "ˀ", "aspiration": "ʰ"} #"labialization": "ᵝ"

l_sounds = [["approx", [["dental", "l̪ l̪̊"], ["postalveolar", "l̠ l̠̊"],
                        ["alveolar", "l l̥"], ["retroflex", "ɭ ɭ̊"],
                        ["velar", "ʟ ʟ̥"], ["uvular", "ʟ̠ ʟ̠̊"],
                        ["palatal", "ʎ ʎ̥"]]],
            ["tap",[["dental", "ɺ̪ ɺ̪̊"], ["postalveolar", "ɺ̠ ɺ̠̊"],
                    ["alveolar", "ɺ ɺ̥"], ["retroflex", "𝼈 𝼈̥"],
                    ["velar", "ʟ̆ ʟ̥̆"], ["uvular", "ʟ̠̆ ʟ̠̥̆"],
                    ["palatal", "ʎ̆ ʎ̥̆"]]],
            ["sibilant",   [["dental", "ʫ̪ ʪ̪"], ["postalveolar", "ʫ̠ ʪ̠"],
                            ["alveolar", "ʫ ʪ"], ["retroflex", "ʫ̢ ʪ̢"]]],
            ["non-sib fr", [["dental", "l̪̝ l̪̝̊"], ["postalveolar", "l̠̝ l̠̝̊"],
                            ["alveolar", "ɮ ɬ"], ["retroflex", "𝼅 ꞎ"],
                            ["velar", "𝼄̬ 𝼄"], ["uvular", "ʟ̠̝ ʟ̠̝̊"],
                            ["palatal", "𝼆̬ 𝼆"]]]]
p_sounds = [["approx", [["dental", "ɹ̪ ɹ̪̊"], ["postalveolar", "ɹ̠ ɹ̠̊"],
                        ["alveolar", "ɹ ɹ̥"], ["retroflex", "ɻ ɻ̊"],
                        ["labiodental", "ʋ ʋ̥"], ["bilabial", "β̞ ɸ̞"],
                        ["velar", "ɰ ɰ̊"], ["uvular", "ʁ̞ χ̞"],
                        ["palatal", "j j̊"], ["pharyngeal", "ʕ̞ ħ̞"],
                        ["glottal", "ʔ̬̞ ʔ̞"]]],
            ["tap",[["dental", "ɾ̪ ɾ̪̊"], ["postalveolar", "ɾ̠ ɾ̠̊"],
                    ["alveolar", "ɾ ɾ̥"], ["retroflex", "ɽ ɽ̊"],
                    ["labiodental", "ⱱ ⱱ̥"], ["bilabial", "ⱱ̟ ⱱ̟̊"],
                    ["velar", "ɡ̆ k̆"], ["uvular", "ɢ̆ q̆"],
                    ["palatal", "j̆ j̊̆"], ["pharyngeal", "ʢ̆ ʜ̆"],
                    ["glottal", "ʔ̬̆ ʔ̆"]]],
            ["trill",  [["dental", "r̪ r̪̊"], ["postalveolar", "r̠ r̠̊"],
                        ["alveolar", "r r̥"], ["retroflex", "ɽ͙ ɽ͙̊"],
                        ["labiodental", "ʙ̪ ʙ̪̊"], ["bilabial", "ʙ ʙ̥"],
                        ["velar", "ɡ͙ k͙"], ["uvular", "ʀ ʀ̥"],
                        ["palatal", "j͙ j͙̊"], ["pharyngeal", "ʢ ʜ"],
                        ["glottal", "ʔ̬͙ ʔ͙"]]],
            ["sibilant",   [["dental", "z̪ s̪"], ["postalveolar", "ʒ ʃ"],
                            ["alveolar", "z s"], ["retroflex", "ʐ ʂ"],
                            ["labiodental", "*z-ᶹ *s-ᶹ"], ["bilabial", "*z-ᵙ *s-ᵙ"],
                            ["velar", "*z-ˠ *s-ˠ"], ["uvular", "*z-ʶ *s-ʶ"],
                            ["palatal", "*z-ʲ *s-ʲ"], ["pharyngeal", "*z-ˤ *s-ˤ"],
                            ["glottal", "*z-ˀ *s-ˀ"]]],
            ["plosive",[["dental", "d̪ t̪"], ["postalveolar", "d̠ t̠"],
                        ["alveolar", "d t"], ["retroflex", "ɖ ʈ"],
                        ["labiodental", "ȸ ȹ"], ["bilabial", "b p"],
                        ["velar", "ɡ k"], ["uvular", "ɢ q"],
                        ["palatal", "ɟ c"], ["pharyngeal", "ʡ̬ ʡ"],
                        ["glottal", "ʔ̬ ʔ"]]],
            ["nasal",  [["dental", "n̪ n̪̊"], ["postalveolar", "n̠ n̠̊"],
                        ["alveolar", "n n̥"], ["retroflex", "ɳ ɳ̊"],
                        ["labiodental", "ɱ ɱ̊"], ["bilabial", "m m̥"],
                        ["velar", "ŋ ŋ̊"], ["uvular", "ɴ ɴ̥"],
                        ["palatal", "ɲ ɲ̊"], ["pharyngeal", "*n-ˤ *n̥-ˤ"],
                        ["glottal", "*n-ˀ *n̥-ˀ"]]],
            ["non-sib fr", [["dental", "ð θ"], ["postalveolar", "ɹ̠̝ ɹ̠̝̊"],
                            ["alveolar", "ð̠ θ̠"], ["retroflex", "ɻ̝ ɻ̝̊"],
                            ["labiodental", "v f"], ["bilabial", "β ɸ"],
                            ["velar", "ɣ x"], ["uvular", "ʁ χ"],
                            ["palatal", "ʝ ç"], ["pharyngeal", "ʕ ħ"],
                            ["glottal", "ɦ h"]]]]


def output_to_symbols_reformat(outputs:list, think_value=0.5, reverse=False, amplify=1.0, bias=0.0):
    # Reverse back
    if reverse:
        new_outputs = []
        for output in outputs:
            new_outputs.append([-i+bias*2+amplify for i in output])
        outputs = new_outputs.copy()
    
    # Max to 1 and min to 0
    if amplify != 1 or bias != 0:
        new_outputs = []
        for output in outputs:
            new_outputs.append([(i-bias)/amplify for i in output])
        outputs = new_outputs.copy()
    
    # All thinking is out
    new_outputs = []
    for output in outputs:
        if output[CRITERIA_TAGS_ID["thi"]] <= think_value: #Not thinking
            new_outputs.append(output)
    outputs = new_outputs.copy()
    
    return outputs

def select_sound(symbols:str, voiceless:bool):
    vd, vl = symbols.split(" ")
    return vl if voiceless else vd

def sound_manner(nc:dict, manner_list:list[list], used_artic:str):
    for manner, sounds in manner_list:
        if nc[manner]:
            sym = select_sound(sounds, nc["vl"])
            nc[manner], nc[used_artic] = False, False
            return nc, sym, True
    return nc, "", False

def sound_artic(nc:dict, artic_list:list[list]):
    for artic, manner_list in artic_list:
        if nc[artic]:
            nc, sym, ok = sound_manner(nc, manner_list, artic)
            if ok: return nc, sym
    return nc, ""
    
def create_new_criteria_output(output):
    nc = {}
    nc["approx"]     = True if output[CRITERIA_TAGS_ID["con"]] < 0.9375 else False
    nc["nasal"]      = False if output[CRITERIA_TAGS_ID["nas"]] < 0.5 else True
    nc["plosive"]    = False if output[CRITERIA_TAGS_ID["plo"]] < 0.5 else True
    nc["sibilant"]   = False if output[CRITERIA_TAGS_ID["sib"]] < 0.5 else True
    nc["trill"]      = False if output[CRITERIA_TAGS_ID["tri"]] < 0.5 else True
    nc["lateral"]    = False if output[CRITERIA_TAGS_ID["lat"]] < 0.5 else True
    nc["bilabial"]   = False if output[CRITERIA_TAGS_ID["bil"]] < 0.5 else True
    nc["dental"]     = False if output[CRITERIA_TAGS_ID["den"]] < 0.5 else True
    nc["alveolar"]   = False if output[CRITERIA_TAGS_ID["alv"]] < 0.5 else True
    nc["retroflex"]  = False if output[CRITERIA_TAGS_ID["ret"]] < 0.5 else True
    nc["palatal"]    = False if output[CRITERIA_TAGS_ID["pal"]] < 0.5 else True
    nc["velar"]      = False if output[CRITERIA_TAGS_ID["vel"]] < 0.5 else True
    nc["uvular"]     = False if output[CRITERIA_TAGS_ID["uvu"]] < 0.5 else True
    nc["pharyngeal"] = False if output[CRITERIA_TAGS_ID["pha"]] < 0.5 else True
    nc["glottal"]    = False if output[CRITERIA_TAGS_ID["glo"]] < 0.5 else True
    nc["aspiration"] = False if output[CRITERIA_TAGS_ID["asp"]] < 0.5 else True
    nc["vl"]         = False if output[CRITERIA_TAGS_ID["vls"]] < 0.5 else True

    curr_crit = output[CRITERIA_TAGS_ID["lbz"]]
    nc["labialization"] = False if curr_crit < 0.75 else True
    nc["half_labialization"] = True if curr_crit > 0.25 and curr_crit <= 0.75 else False

    nc["tap"], nc["labiodental"], nc["postalveolar"], nc["non-sib fr"] = False, False, False, False
    if nc["plosive"] and nc["trill"]:
        nc["tap"], nc["plosive"], nc["trill"] = True, False, False
    if nc["bilabial"] and nc["dental"]:
        nc["labiodental"], nc["bilabial"], nc["dental"], nc["alveolar"] = True, False, False, False
    if nc["alveolar"] and nc["retroflex"]:
        nc["postalveolar"], nc["alveolar"], nc["retroflex"] = True, False, False
    if nc["dental"] and nc["alveolar"]:
        nc["dental"], nc["alveolar"] = True, False
    
    nc["non-sib fr"] = not (nc["approx"] or nc["tap"] or nc["trill"] or
                            nc["sibilant"] or nc["plosive"] or nc["nasal"])
    return nc

def output_to_symbols(outputs:list, think_value=0.5, ignore_first=False, reverse=False, amplify=1.0, bias=0.0, spacing=""):
    if ignore_first: outputs.pop(0)
    outputs = output_to_symbols_reformat(outputs, think_value, reverse, amplify, bias)
    whole_symbol_notation = ""
    for output in outputs:
        curr_sym = ""
        is_vowel = False
        is_consonant = False
        is_space = False
        if output[CRITERIA_TAGS_ID["spa"]] >= 0.5: #Space
            is_space = True
            curr_sym = " " if output[CRITERIA_TAGS_ID["lon"]] < 0.5 else "|"
        elif output[CRITERIA_TAGS_ID["con"]] < 0.8125: # Vowel
            is_vowel = True
        else:
            is_consonant = True
        
        if is_consonant:
            # Selecting complex
            nc = create_new_criteria_output(output)

            if nc["alveolar"] and nc["velar"] and nc["lateral"] and nc["approx"]:
                curr_sym = select_sound("ɫ ɫ̥", nc["vl"])
                nc["alveolar"], nc["velar"], nc["lateral"], nc["approx"] = False, False, False, False
            elif nc["labialization"] and nc["velar"] and nc["approx"]:
                curr_sym = select_sound("w ʍ", nc["vl"])
                nc["labialization"], nc["velar"], nc["approx"] = False, False, False
            elif nc["labialization"] and nc["palatal"] and nc["approx"]:
                curr_sym = select_sound("ɥ ɥ̊", nc["vl"])
                nc["labialization"], nc["palatal"], nc["approx"] = False, False, False
            elif nc["postalveolar"] and nc["palatal"] and nc["sibilant"] and not nc["approx"]:
                curr_sym = select_sound("ʑ ɕ", nc["vl"])
                nc["postalveolar"], nc["palatal"], nc["sibilant"] = False, False, False
            else:
                if nc["lateral"]:
                    nc, curr_sym = sound_artic(nc, l_sounds)
                    if curr_sym != "":
                        nc["lateral"] = False
                else:
                    nc, curr_sym = sound_artic(nc, p_sounds)
            
        if is_vowel: # Vowel
            nc = create_new_criteria_output(output)
            nc["approx"] = False

            roundness = 2 if nc["labialization"] else 1 if nc["half_labialization"] else 0
            nc["labialization"], nc["half_labialization"] = False, False

            backness = 1 if nc["palatal"] == nc["velar"] else 0 if nc["palatal"] else 2
            nc["palatal"], nc["velar"] = False, False
            
            curr_crit = output[CRITERIA_TAGS_ID["con"]]
            curr_crit = 0 if curr_crit < 0 else 0.75 if curr_crit > 0.75 else curr_crit
            curr_crit = curr_crit * 16 + 1
            closeness = 6 - int(curr_crit // 2)
            
            curr_sym = vowels_table[closeness][backness][roundness]
            if nc["retroflex"]:
                if "ə" in curr_sym:
                    curr_sym = curr_sym.replace("ə", "ɚ")
                elif "ɜ" in curr_sym:
                    curr_sym = curr_sym.replace("ɜ", "ɝ")
                else:
                    curr_sym += "˞"
            nc["retroflex"] = False
            
            if nc["vl"]:
                if "y" in curr_sym or "̹" in curr_sym or "̞" in curr_sym:
                    curr_sym += "̊"
                else:
                    curr_sym += "̥"
        
        if not is_space:
            if curr_sym == "":
                curr_sym = "◌"
            
            curr_sym_split = curr_sym.split("-", 1)
            if len(curr_sym_split) == 1: curr_sym_split.append("")
            
            for i in MODS_TABLE_ADD:
                if nc[i]:
                    curr_sym_split[0] += MODS_TABLE_ADD[i]
                    nc[i] = False
            for i in SUB_TABLE_ADD:
                if nc[i]:
                    curr_sym_split[1] += SUB_TABLE_ADD[i]
                    nc[i] = False
            curr_sym = curr_sym_split[0]+curr_sym_split[1]

            # if "ᵝ" in curr_sym and "ˠ" in curr_sym:
            #     curr_sym = curr_sym.replace("ᵝ", "ʷ")
            #     curr_sym = curr_sym.replace("ˠ", "")
            
            if SUB_TABLE_ADD["labialization"] in curr_sym and SUB_TABLE_ADD["palatal"] in curr_sym:
                curr_sym = curr_sym.replace(SUB_TABLE_ADD["labialization"], "ᶣ")
                curr_sym = curr_sym.replace(SUB_TABLE_ADD["palatal"], "")

            # Long sound and stress
            if output[CRITERIA_TAGS_ID["lon"]] >= 0.5:
                curr_sym += "ː"
            if output[CRITERIA_TAGS_ID["str"]] >= 0.5:
                curr_sym = "ˈ"+curr_sym
        
        # Adding spacing
        curr_sym += spacing

        whole_symbol_notation += curr_sym
    return whole_symbol_notation
