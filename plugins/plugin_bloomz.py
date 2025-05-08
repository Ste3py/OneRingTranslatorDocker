# bloomz plugin
# author: Vladislav Janvarev

# from https://huggingface.co/bigscience/bloomz-1b7

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
        "name": "Bloomz Translate", # name
        "version": "2.0", # version

        "translate": {
            "bloomz": (init,translate) # 1 function - init, 2 - translate
        },

        "default_options": {
            "model": "bigscience/bloomz-1b7",  # key model
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
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    global model, tokenizer

    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(core.plugin_options(modname).get("model"))
    model = AutoModelForCausalLM.from_pretrained(core.plugin_options(modname).get("model")).to(to_device)


    pass


def translate(core:OneRingCore, text:str, from_lang:str = "", to_lang:str = "", add_params:str = ""):
    # from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    from_full_lang = core.dict_2let_to_lang.get(from_lang)
    to_full_lang = core.dict_2let_to_lang.get(to_lang)

    input_str =f"Translate this text from {from_full_lang} to {to_full_lang}: {text}"
    inputs = tokenizer.encode(input_str, return_tensors="pt").to(to_device)
    outputs = model.generate(inputs, max_new_tokens=len(input_str)*3)
    res = str(tokenizer.decode(outputs[0]))[len(input_str):]

    #ar_res = res.split("</s>")

    res0 = res.replace("</s>"," ").strip()



    return res0

