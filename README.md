# Localizr
I'm too lazy to update the localization files and It's too prone to error because not all developers understand all those words. So give the Translator an access to a page where they can input those translations and developers will just do their job by fetching it automatically.

#### DEMO

You can access the demo pages with this credential:
```
username: demo
password: localizr
```

###### Admin page
http://app-localizr.herokuapp.com

###### Strings Generator

Format:
```
http://app-localizr.herokuapp.com/app/{app_slug}-{locale_code}
```

http://app-localizr.herokuapp.com/app/demo-en

http://app-localizr.herokuapp.com/app/demo-ja


#### AUTO-DEPLOY TO HEROKU

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/michaelhenry/localizr)


## Format

#### iOS

```txt
"key" = "value";
```

Eg.

http://app-localizr.herokuapp.com/app/demo-ja?format=ios


#### Android

```xml
<resources>
  <string name="key">value</string>
</resources>
```

Eg.

http://app-localizr.herokuapp.com/app/demo-ja?format=android

## TODO:

- [x] iOS format support
- [x] Android format support
- [ ] Import content via CSV file
- [ ] Able to use google translate for some missing translations.

## Author

Michael Henry Pantaleon, me@iamkel.net

## License

Localizr is available under the MIT license. See the LICENSE file for more info.
