# lingvanex Translate plugin
# author: Vladislav Janvarev

from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "lingvanex Translator", # name
        "version": "1.1", # version

        "default_options": {
            "api_key": "",  #
        },

        "translate": {
            "lingvanex": (init, translate)  # 1 function - init, 2 - translate
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

    api_key:str = core.plugin_options(modname).get("api_key")

    import requests

    url = "https://api-b2b.backenster.com/b1/api/v3/translate"

    payload = {
        "platform": "api",
        "from": from_lang,
        "to": to_lang,
        "data": text
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": api_key
    }

    response = requests.post(url, json=payload, headers=headers)

    #print(respons*e.text)
    response_json = response.json()

    if response_json.get("err") is not None:
        raise ValueError("ERR in ligvanex server call: "+response_json.get("err"))
    #print(response_json)


    return response_json["result"]
