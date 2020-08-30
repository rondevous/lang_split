# Translation split
Split your Telegram language file into **translated** and **untranslated**. Import the **translated** file for a clean recent-translations history. The **untranslated** file can be used for offline translation.

All apps on the [Telegram translations platform]((https://translations.telegram.org)) are supported.

## Why do I need this?
- Is your recent translations messed up?
- Did you make changes to an exported translation file, but don't want to import 2000 untranslated strings?

[lang_split.py](https://github.com/rondevous/lang_split/raw/master/lang_split.py) will give you a clean history of your recent-translations!

### Setup:
1. Download and Install [Python 3](https://www.python.org/downloads)
2. Download [lang_split.py](https://github.com/rondevous/lang_split/raw/master/lang_split.py)
_(right click the link > Save link as)_

### Preparations:
1. Export your language from [translations.telegram.org/**langname/appname**](https://translations.telegram.org)
2. Also export its base language.
* If your base language is English, export [English](https://translations.telegram.org/en), if its Russian, export [Russian](https://translations.telegram.org/ru).
* If your language is official, your base language is English by default.
3. Keep all 3 files in the same folder:
```
lang_split.py
language_file.xml
base_language_file.xml
```

## How to use:
Open command prompt / terminal and Enter the command you need (do not copy the `$`)

Tip: Pressing 'Tab' in the terminal will autocomplete the file name.

**Split the translations**
```
$ python lang_split.py --lang android_customlang.xml --base android_en.xml
```

**Help message**
```
$ python lang_split.py --help
```

**To avoid importing the same translations, use --base with a recent export of your language from the [translations platform](https://translations.telegram.org)**
```
$ python lang_split.py --lang android_x_customlang_edited.xml --base android_x_customlang_v112332.xml
```

### Extra options
```
--translated
--untranslated
```
These will show the translations in the terminal. See the examples below:

**Split and display translated**
```
$ python lang_split.py --translated --lang tdesktop_customlang.strings --base tdesktop_en_v324453.strings
```

**Split and display untranslated**
```
$ python lang_split.py --untranslated --lang ios_customlang.strings --base ios_en_v324453.strings
```

## More tools and support
Join us in the [Translation Platform Tools](https://t.me/TranslationTools) group

