# Localizr
[wip] Locale files generator. because I hate updating locale files manually. It's prone to error because not all developers understand all those words. So give the Translator an access to a page where they can input those translations and developers will just do their job by fetching it automatically.


## DEPLOY TO HEROKU

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/michaelhenry/localizr

## Format

#### iOS

```txt
"key" = "value";
```

#### Android

```xml
<resources>
  <string name="key">value</string>
</resources>
```

## Models
- App, ofcourse we do have different applications.
- Platform,  (ios, android, Django, where we can also define the format so it is flexible). 
- Locale, the list of localizations that we are supporting.
- KVStore, where we store the key-value pair.

## Author

Michael Henry Pantaleon, me@iamkel.net

## License

Localizr is available under the MIT license. See the LICENSE file for more info.
