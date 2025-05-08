# Translate plugin throw KoboldAPI interface
# KoboldAPI is a REST interface for lots of LLM servers (like koboldcpp, text-generation-webui)
# author: Vladislav Janvarev

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "KoboldAPI Translator", # name
        "version": "2.0", # version

        "default_options": {
            "custom_url": "http://localhost:5000/",  #
            "prompt": "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n### Instruction:\nTranslate this text from {0} to {1}:\n\n{2}\n\n\n### Response:"
        },

        "translate": {
            "koboldapi_translate": (init,translate) # 1 function - init, 2 - translate
        }
    }
    return manifest

def start_with_options(core:OneRingCore, manifest:dict):

    # PATCH ENV → JSON
    import os
    import json

    PLUGIN_NAME_FULL = os.path.splitext(os.path.basename(__file__))[0]

    if PLUGIN_NAME_FULL.startswith("plugin_"):
        PLUGIN_NAME = PLUGIN_NAME_FULL[len("plugin_"):]
    else:
        PLUGIN_NAME = PLUGIN_NAME_FULL

    env_var = f"{PLUGIN_NAME.upper()}_CONFIG"
    plugin_config_env = os.getenv(env_var)

    if plugin_config_env:
        print(f"== {env_var} détecté, écriture dans options/{PLUGIN_NAME}.json ==")
        try:
            options_env = json.loads(plugin_config_env)
            os.makedirs("options", exist_ok=True)
            with open(f"options/{PLUGIN_NAME}.json", "w", encoding="utf-8") as f:
                json.dump(options_env, f, indent=2, ensure_ascii=False)
            manifest["options"] = options_env
        except Exception as e:
            print(f"Erreur lors de l'écriture de {PLUGIN_NAME}.json à partir de {env_var} :", e)
    
    pass
def init(core:OneRingCore):
    pass

def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    options = core.plugin_options(modname)

    import json
    custom_stopping_strings = ["\n\n","\n### "]
    params = {
        'max_new_tokens': int(len(text)*1.5),
        'max_length': int(len(text)*1.5),
        'do_sample': True,
        'temperature': 0.7,
        'top_p': 0.2,
        'typical_p': 1,
        'repetition_penalty': 1.18,
        'encoder_repetition_penalty': 1.0,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': True,
        'seed': -1,
        'add_bos_token': True,
        'custom_stopping_strings': custom_stopping_strings,
        'stop_sequence': custom_stopping_strings,
        'truncation_length': 2048,
        'ban_eos_token': False,
    }

    from_full_lang = core.dict_2let_to_lang.get(from_lang)
    to_full_lang = core.dict_2let_to_lang.get(to_lang)


    from time import time
    start = time()
    # # Input prompt for Alpaca
    # tpl = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n"
    # tpl += f"### Instruction:\nTranslate this text from {from_full_lang} to {to_full_lang}:\n\n"
    # #tpl += "### Input:\n{0}\n\n\n\n"
    # tpl += "{0}\n\n\n"
    # tpl += "### Response:"

    prompt = str(options["prompt"]).format(from_full_lang,to_full_lang,text)
    print(prompt)

    params["prompt"] = prompt
    #print(params)

    import requests
    url = f"{core.plugin_options(modname).get('custom_url')}api/v1/generate"
    #print(url)
    response = requests.post(url, json=params)

    if response.status_code != 200:
        return "ERROR in call KoboldAPI url: status code {0}".format(response.status_code)

    #print(response)

    reply:str = response.json()["results"][0]['text']
    reply = reply.strip()

    end = time()
    #print("Duration: {0}".format(end - start))

    for stop_string in custom_stopping_strings:
        if stop_string in reply:
            res = reply.split(stop_string)
            reply = res[0]

    #print(reply)

    return reply