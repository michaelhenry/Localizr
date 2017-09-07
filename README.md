# Localizr
[wip] Locale files generator. because I hate updating locale files manually.


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
