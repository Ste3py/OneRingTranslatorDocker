# Core plugin
# author: Vladislav Janvarev
import os
import json
from oneringcore import OneRingCore

# start function
def start(core:OneRingCore):
    manifest = {
        "name": "Core plugin",
        "version": "1.5",

        # this is DEFAULT options
        # ACTUAL options is in options/<plugin_name>.json after first run
        "default_options": {
            "default_translate_plugin": "google_translate", # default translation engine. Will be auto inited on start
            "init_on_start": "",  # additional list of engines, that must be init on start, separated by ","
            "default_from_lang": "es", # default from language
            "default_to_lang": "en", # default to language
            "api_keys_allowed": [], # set of API keys. If empty - no API key required.
            "debug_input_output": False, # allow debug print input and output in console
            "allow_multithread": True, # allow multithread run of translation engine
            "user_lang": "", # standart user language. Replaces "user" in to_lang or from_lang API params
            "cache_is_use": True, # use cache?
            "cache_save_every": 5,  # every X elements save cache to disk
            "cache_per_model": True, # differentiate cache per model
            "default_translate_router": { # routing for default translation engine on different language pairs
                "fr->es": "no_translate", # this is just an example, adjust in to your needs
                "fr->fn": "no_translate2", # asterisk supported like *->fr
            }
        },

    }
    return manifest

def start_with_options(core:OneRingCore, manifest:dict):
    # Check if CORE_CONFIG env exists
    core_config_env = os.getenv('CORE_CONFIG')

    if core_config_env:
        print("== CORE_CONFIG détecté, écriture dans options/core.json ==")
        try:
            options_env = json.loads(core_config_env)
            os.makedirs("options", exist_ok=True)
            with open("options/core.json", "w", encoding="utf-8") as f:
                json.dump(options_env, f, indent=2, ensure_ascii=False)
            manifest["options"] = options_env
        except Exception as e:
            print("Erreur lors de l'écriture du core.json à partir de CORE_CONFIG :", e)

    options = manifest["options"]

    core.default_translator = options["default_translate_plugin"]
    core.default_from_lang = options["default_from_lang"]
    core.default_to_lang = options["default_to_lang"]
    core.default_translate_router = options["default_translate_router"]

    core.api_keys_allowed = options["api_keys_allowed"]

    core.is_multithread = options["allow_multithread"]
    core.is_debug_input_output = options["debug_input_output"]

    core.user_lang = options["user_lang"]

    core.cache_is_use = options["cache_is_use"]
    core.cache_save_every = options["cache_save_every"]
    core.cache_per_model = options["cache_per_model"]

    core.init_on_start = options["init_on_start"]

    return manifest
