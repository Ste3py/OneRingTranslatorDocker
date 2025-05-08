# WEB API for translation

# Fork By SteepyTheFrenchMaker :

**This fork goal is to make OneRingTranslator running inside a docker container**



Every JSON file in the app has a default state.  
If you don't set the corresponding ENV variable for a plugin, it will load its default values.  
If you set the ENV variable, the values will overwrite the defaults at runtime.  
So, if you don't want to overwrite a JSON, just leave the ENV variable as "" (empty).

| ENV VAR                         | Default Value | Description                                       |
|--------------------------------|---------------|---------------------------------------------------|
| HOST                           | 0.0.0.0       | IP address of the WebUI                           |
| PORT                           | 4990          | Port of the WebUI                                 |
| OFFLINE_MODE             | false | can be set on true and gonna download the requirements-offline.txt    |
| CORE_CONFIG                    | ""            | JSON for core.json                                |
| BLOOMZ_CONFIG                  | ""            | JSON for bloomz.json                              |
| CUSTOM_LIBRE_TRANSLATE_CONFIG  | ""            | JSON for custom_libre_translate.json              |
| DEEPL_CONFIG                   | ""            | JSON for deepl.json                               |
| FB_MBART50_CONFIG              | ""            | JSON for fb_mbart50.json                         |
| FB_NLLB_CTRANSLATE2_CONFIG     | ""            | JSON for fb_nllb_ctranslate2.json                |
| FB_NLLB_TRANSLATE_CONFIG       | ""            | JSON for fb_nllb_translate.json                  |
| GEMINI_CHAT_CONFIG             | ""            | JSON for gemini_chat.json                        |
| GOOGLE_TRANSLATE_CONFIG        | ""            | JSON for google_translate.json                   |
| KOBOLDAPI_TRANSLATE_CONFIG     | ""            | JSON for koboldapi_translate.json                |
| LIBRE_TRANSLATE_CONFIG         | ""            | JSON for libre_translate.json                    |
| LINGVANEX_CONFIG               | ""            | JSON for lingvanex.json                          |
| MULTI_SOURCES_CONFIG           | ""            | JSON for multi_sources.json                      |
| NO_TRANSLATE_CONFIG            | ""            | JSON for no_translate.json                       |
| NO_TRANSLATE2_CONFIG           | ""            | JSON for no_translate2.json                      |
| OPENAI_CHAT_CONFIG             | ""            | JSON for openai_chat.json                        |
| OPUS_MT_CONFIG                 | ""            | JSON for opus_mt.json                            |
| T5_MT_CONFIG                   | ""            | JSON for t5_mt.json                              |
| USE_MID_LANG_CONFIG            | ""            | JSON for use_mid_lang.json                       |
| VSEGPT_CHAT_CONFIG             | ""            | JSON for vsegpt_chat.json                       |


[Available en docker hub](https://hub.docker.com/r/steepythefrenchmaker/oneringtranslatordocker)

# ORIGINAL README

Simple WEB API REST service for translation.

Features:
- **Plugin support**. If you misses some translation engine, you can add it yourself! 
- **Full offline translation (optionally).** You can setup your own offline https://github.com/LibreTranslate/LibreTranslate service and target this service to use it as endpoint. Or use effective FB NLLB neuronet.
- **Ready to use**. By default use Google Translate service, and ready to use.
- **Simple REST API interface** throw FastApi and openapi.json interface. After install go to `http://127.0.0.1:4990/docs` to see examples.
- **API keys**. (Disabled by default) You can restrict access to your service by set up a list of API keys, needed to access the service.
- **Cache translations** (if necessary)
- **Automatic BLEU and COMET estimation of translation quality** 
  - If you want to test different plugins translation quality on your pair of languages - you can do it! (Supported over 100 languages from FLORES dataset)
  - If you have your own plugin - you can compare it with others!  
- **Unique World Best results by multi_sources plugin!**
  - We have a plugin that gains translations from multiple sources, then estimate them and return only the best
  - It gains the best COMET translation evaluation score against other plugins.
- **Translation routing** Use different translation engines on different language pairs.

## Links

- [Supported translators](#known-supported-translators)
- [Known OneRingTranslator usages](#known-usages)
- **[Install and run](/docs_md/INSTALL.md)**
- [Base settings and plugin logic](/docs_md/SETTINGS.md)
- [Plugins options](/docs_md/PLUGINS.md)
- [REST API usage examples](/docs_md/API.md)
- **[Benchmarks (BLEU, COMET) for plugins translation quality](/docs_md/ESTIMATIONS.md)** 
Use it to choose what plugin you want to run for your own translation task. Also you can do your own measures with script here.   


## Known supported translators

### Online

- Google Translate (free)
- Deepl Translate (require API key)
  - [Alt version](https://github.com/janvarev/onering_plugins_chrome_dev) that doesn't require API key 
- Libre Translate (online free, but slow)
- OpenAI Chat interface (ChatGPT, GPT-4), (online or offline emulation)
  - API key required, if you want to connect to OpenAI servers
  - Otherwise, you can connect through this interface to local OpenAI emulation servers.
- Yandex translation ([through browser manipulation](https://github.com/janvarev/onering_plugins_chrome_dev))
- [Lingvanex](https://lingvanex.com/)
- Translation via [VseGPT](https://vsegpt.ru/) LLM online models (require API key):
  - ChatGPT
  - GPT-4
  - Claude Instant v1
  - Claude v2
  - Google: PaLM 2 Bison

### Offline

- Libre Translate (online or offline)
- FB NLLB neuronet (offline)
  - Also support [CTranslate2](https://opennmt.net/CTranslate2/index.html) realization of neuronet
- FB MBart50 (imho worser then NLLB) 
- KoboldAPI endpoint (offline mostly due to target localhost)
  - KoboldAPI is a REST interface for lots of LLM servers (like [koboldcpp](https://github.com/LostRuins/koboldcpp/releases), [text-generation-webui](https://github.com/oobabooga/text-generation-webui))
  - If you load some LLM model inside this LLM server, you can translate texts using them!
  - (Now plugin uses Alpaca template to set translation task. Change it if you want)
- OpenAI Chat interface (ChatGPT), (online or offline emulation)
  - API key required, if you want to connect to OpenAI servers
  - Otherwise, you can connect through this interface to local OpenAI emulation servers.
- No Translate (offline) - dummy translator to compare with
- Opus MT
- Bloomz (https://huggingface.co/bigscience/bloomz-1b7)

### Synthetic 

- multi_source - get translations from other plugins, and choose the best one
- use_mid_lang - translate with other plugins by chaining translating to middle-language, usually English (FromLang->En->ToLang)

## Known usages

- https://github.com/HIllya51/LunaTranslator - automatic game translation tool
- https://github.com/janvarev/multi_translate - oobabooga/text-generation-webui plugin for translate conversation with LLM (Large Language Models) UserLanguage<->English
- https://github.com/janvarev/privateGPT - privateGPT multilanguage fork
- You can use it with https://github.com/translate-tools/linguist Web browser translation to translate web pages
  - You'll need to add custom translator with this JS code: https://gist.github.com/janvarev/314b13e4d44d5a0cc349385ee85a4f58
- https://github.com/SillyTavern/SillyTavern - multi-LLM frontend




## Thanks to

https://github.com/jenil/chota Chota project for awesome CSS
