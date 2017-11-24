# Localizr

[![Build Status](https://travis-ci.org/michaelhenry/Localizr.svg?branch=master)](https://travis-ci.org/michaelhenry/Localizr)

Localizr is a DSL that handles and automates localization files. Basically we give limited access to the translators to let them input or upload different keystrings and we developer will just fetch it on development or deployment only when if there is an update or changes. This will lessen or prevent the mistake that developer made because he/she has no clue what are those words is and most of them (including me, but not all) are just copy pasting those words (especially when it comes to chinese or japanese characters) from excel to the Localizable.strings via Xcode.
      

## Features
- Multi-App support. reusable keys for different applications.
- Android and IOS support.
- Integrated with `Fastlane actions`. (for IOS, `Fastlane actions localizr`) 
- Default fallback for missing localizations.
- Export and import to different file format.
- Easy deployment: [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/michaelhenry/localizr)

## DEMO
- http://localizr.iamkel.net
You can access the demo pages with this credential:
```
username: demo
password: localizr
```


## For Developers
### Strings Generator
```
http://localizr.iamkel.net/app/{app_slug}.{locale_code}
```
- http://localizr.iamkel.net/app/demo.en
- http://localizr.iamkel.net/app/demo.ja

### Format
#### iOS
- http://localizr.iamkel.net/app/demo.ja?format=ios

### Android
- http://localizr.iamkel.net/app/demo.ja?format=android

## For Non-Developers
### How to use Localizr?

1. Create different `Locales` set the `name` and the `code`.
2. Create an `App` and set the `base_locale` if you want to have a fallback for missing `localized strings`.
3. Create Different `Keys`.
4. Match the `Keys` with the `App` so you can re-use the keys to other apps too.
5. Finally, populate the `localized strings` .


#### Does it look difficult? 
### Then try to use the importer (csv, xls, xlsx, tsv, json, yaml).
You can find the sample csv files in the [sample_data](/sample_data) folder.

1. Import the `Locales.csv` to `Locales` section.
2. Import the `Apps.csv` to `Apps` section.
3. Import the `App's Keys.csv` to `App 's Keys` section.
4. Import the `Localized String.csv` to `Localized String` section.

### How about exporting?
Just find the `EXPORT` button, select the `format` and that's it.


## Recommendation, Automation and Deployment:
With using `CI` and `Fastlane`, create a script or use `fastlane actions localizr` to download and update all the localization strings before `gym` method, So we can always make sure that all strings are updated. 


## TODO:

- [x] iOS format support
- [x] Android format support
- [x] Import/Export contents via CSV file
- [x] CI
- [x] Test cases
- [ ] Interactive UI.
- [ ] Able to use google translate for some missing translations.
- [ ] Docker container support.

## Author

Michael Henry Pantaleon, me@iamkel.net

## License

Localizr is available under the MIT license. See the LICENSE file for more info.
