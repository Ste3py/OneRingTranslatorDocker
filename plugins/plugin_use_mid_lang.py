# Use mid (mediator) language
# Translate in two phases: from lang->mediator lang, mediator lang->to lang
# author: Vladislav Janvarev

from oneringcore import OneRingCore
import os
import time

modname = os.path.basename(__file__)[:-3] # calculating modname

# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "Use mediator language", # name
        "version": "1.1", # version

        "default_options": {
            "model": "google_translate->deepl",  # 1 phase plugin, 2 phase plugin
            #  1 phase from lang->mediator lang,
            #  2 phase mediator lang->to lang
            "mid_lang": "en",
        },

        "translate": {
            "use_mid_lang": (init,translate) # 1 function - init, 2 - translate
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
    plugins: str = core.plugin_options(modname).get("model").split("->")
    mid_lang: str = core.plugin_options(modname).get("mid_lang")
    res1 = core.translate(text,from_lang,mid_lang,plugins[0]).get("result")
    #print(from_lang,mid_lang,res1)
    #time.sleep(0.02)
    res2 = core.translate(res1,mid_lang,to_lang,plugins[1]).get("result")
    #print(mid_lang,to_lang,res2)

    return res2
