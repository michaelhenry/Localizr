# Localizr

[![Build Status](https://travis-ci.org/michaelhenry/Localizr.svg?branch=master)](https://travis-ci.org/michaelhenry/Localizr)


I'm too lazy to update the localization files and It's too prone to error because not all developers understand all those words. So give the Translator an access to a page where they can input those translations and developers will just do their job by fetching it automatically.

#### DEMO

You can access the demo pages with this credential:
```
username: demo
password: localizr
```

###### Admin page
http://localizr.iamkel.net

###### Strings Generator

Format:
```
http://localizr.iamkel.net/app/{app_slug}-{locale_code}
```

http://localizr.iamkel.net/app/demo-en

http://localizr.iamkel.net/app/demo-ja


#### AUTO-DEPLOY TO HEROKU

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/michaelhenry/localizr)


## Format

#### iOS

```txt
"key" = "value";
```

Eg.

http://localizr.iamkel.net/app/demo-ja?format=ios


#### Android

```xml
<resources>
  <string name="key">value</string>
</resources>
```

Eg.

http://localizr.iamkel.net/app/demo-ja?format=android


## Recommendation, Automation and Deployment:
With using `CI` and `Fastlane`, create a script that will download and update all the localization strings before `gym` method, So we can always make sure that all strings are updated. 


## TODO:

- [x] iOS format support
- [x] Android format support
- [x] Import/Export contents via CSV file
- [x] CI
- [x] Test cases
- [ ] Interactive UI.
- [ ] Able to use google translate for some missing translations.

## Author

Michael Henry Pantaleon, me@iamkel.net

## License

Localizr is available under the MIT license. See the LICENSE file for more info.
