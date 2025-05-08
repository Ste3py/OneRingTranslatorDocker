# t5 mt
# author: Vladislav Janvarev


from oneringcore import OneRingCore
import os

modname = os.path.basename(__file__)[:-3] # calculating modname

model = None
tokenizer = None

cuda_opt = -1
to_device = "cpu"
# start function
def start(core:OneRingCore):
    manifest = { # plugin settings
        "name": "T5 MT Translate", # name
        "version": "1.0", # version

        "translate": {
            "t5_mt": (init,translate) # 1 function - init, 2 - translate
        },

        "default_options": {
            "model": "utrobinmv/t5_translate_en_ru_zh_large_1024",  # key model
            "cuda": -1, # -1 if you want run on CPU, 0 - if on CUDA
       },
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

    global cuda_opt
    global to_device
    cuda_opt = manifest["options"].get("cuda")
    if cuda_opt == -1:
        to_device = "cpu"
    else:
        to_device = "cuda:{0}".format(cuda_opt)
    pass

def init(core:OneRingCore):
    from transformers import T5ForConditionalGeneration, T5Tokenizer

    global model, tokenizer

    #print(to_device)
    model_name = core.plugin_options(modname).get("model")
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name).to(to_device)


def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    src_text = [f"translate to {to_lang}: "+text]
    translated = model.generate(**tokenizer(src_text, return_tensors="pt").to(to_device))
    res = tokenizer.decode(translated[0], skip_special_tokens=True)
    return res