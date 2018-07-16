# Localizr

[![Build Status](https://travis-ci.org/michaelhenry/Localizr.svg?branch=master)](https://travis-ci.org/michaelhenry/Localizr)
[![Twitter](https://img.shields.io/badge/twitter-@michaelhenry119-blue.svg?style=flat)](https://twitter.com/michaelhenry119)
[![Docker](https://img.shields.io/badge/docker-michaelhenry119/localizr-red.svg?style=flat)](https://hub.docker.com/r/michaelhenry119/localizr/tags/)
[![Version](https://img.shields.io/badge/version-1.2-yellow.svg?style=flat)](#)


Localizr is a Tool that handles and automates localization files. Basically we give limited access to the translators to let them input or upload different keystrings and the developer will just fetch it on development or deployment only when if there is an update or changes. This will lessen or prevent the mistake that developer made because he/she has no clue what are those words are and most of them (including me, but not all) are just copy pasting those words (especially when it comes to chinese or japanese characters) from excel to the Localizable.strings via Xcode.
      

## Features
- Multi-App support. reusable keys for different applications.
- Android and IOS support.
- Integrated with `Fastlane actions`. (`Fastlane actions localizr`) 
- Default fallback for missing localizations.
- Export and import to different file format.
- Easy deployment: [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/michaelhenry/localizr)
- Dockerized: `docker pull michaelhenry119/localizr`
- Static files hosted in AWS S3 (Optional)
- Snapshots


## DEMO
- http://localizr.iamkel.net
You can access the demo pages with this credential:
```
username: demo
password: localizr
```


## IOS Client
I have created a demo IOS App, You can pull it from [Localizr.swift](https://github.com/michaelhenry/Localizr.swift).


## For Developers
### Strings Generator
```
http://{your_server.com}/app/{app_slug}.{locale_code}
```
- http://localizr.iamkel.net/app/demo.en
- http://localizr.iamkel.net/app/demo.ja

### Format
#### iOS
- http://localizr.iamkel.net/app/demo.ja?format=ios

### Android
- http://localizr.iamkel.net/app/demo.ja?format=android

### Integrate to your Android or IOS Project?
By using `Fastlane`. Currently `localizr` action is not officially available in `fastlane` repo, so you have to manually grab it from here  [fastlane/actions](/fastlane/actions) and paste the `actions` folder directly to your project 's `fastlane` folder in order to make this available to your local.
here is the shortcut:
```bash
# from your workplace root folder:
$ curl -o fastlane/actions/localizr.rb https://raw.githubusercontent.com/michaelhenry/Localizr/master/fastlane/actions/localizr.rb
```

```bash
$ fastlane actions localizr
```
![fastlane actions localizr](docs/images/fastlane_actions_localizr.png)

#### Sample configuration on IOS
```ruby
desc "Submit build to TestFlight."
lane :beta do
  increment_build_number
  # ...
  localizr(
    localizr_server: 'http://your_localizr_server',
    localizr_api_token: 'your-auth-token-from-admin-page',
    locale_codes:  'en,ja,pt,zh,es',
    localizr_app_slug: 'your-app-slug',
    output_target_path: 'ExampleApp',
    platform: 'ios',
  )
  gym
  # ...
end
```

#### Sample configuration on Android
```ruby
lane :beta do
  localizr(
    localizr_server: 'http://your_localizr_server',
    localizr_api_token: 'your-auth-token-from-admin-page',
    locale_codes:  'en,ja,pt,zh,es',
    localizr_app_slug: 'your-app-slug',
    output_target_path: 'res'
  ),
  gradle(
    task: 'assemble',
    build_type: 'Release'
  )
  # ...
end
```

### You can also use environment variables if you dont want to configure it from Fastfile:

```bash
export FL_LOCALIZR_SERVER='http://your_localizr_server'
export FL_LOCALIZR_API_TOKEN='your-auth-token-from-admin-page'
export FL_LOCALIZR_APP_SLUG='your-app-slug'
export FL_LOCALIZR_BASE_LOCALE_CODE='en'
export FL_LOCALIZR_LOCALE_CODES='en,es,ja,zh,pt'
export FL_LOCALIZR_PLATFORM='ios'
export FL_LOCALIZR_OUTPUT_TARGET_PATH='ExampleApp'
```

Example:

```ruby
desc "Submit build to TestFlight."
lane :beta do
  increment_build_number
  # ...
  localizr
  gym
  # ...
end
```

### S3 Configuration
This is optional, but you can enable this by providing valid information for the following in the environment variables.
```bash
export AWS_ACCESS_KEY_ID='Your aws access key id'
export AWS_SECRET_ACCESS_KEY='Your secret key'
export AWS_STORAGE_BUCKET_NAME='Name of the bucket'
```

## For Non-Developers, Translators or even Developers.
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

![import admin import](docs/images/admin_localized_strings_import.png)

![import button](docs/images/admin_import.png)

![import change diff](docs/images/admin_import_compare.png)


### How about exporting?
Just find the `EXPORT` button, select the `format` and that's it.

## Deployment
### Using Heroku
Just click this button >++> [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/michaelhenry/localizr)



### Using Docker
sample config of `docker-compose.yml`
```yml
version: '3'

services:
  db:
    image: postgres:9.4
    volumes:
      - pg-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"  
    environment:
      - POSTGRES_PASSWORD=your_db_password

  localizr:
    image: michaelhenry119/localizr:latest
    container_name: localizr
    ports:
      - "80:8001"
    environment:
      # Reference: postgres://USER:PASSWORD@HOST:PORT/NAME, this example is using the default postgres database.
      - DATABASE_URL=postgres://postgres:your_db_password@db:5432/postgres
      # You have to define your host name here to prevent any random attacks.
      - ALLOWED_HOSTS=0.0.0.0,localizr.domain.com,or_any_domain
      # This is optional, you can assign a default then change it later from the admin page. 
      # Or you can do it programatically after you mount the image.
      - ADMIN_USERNAME=admin
      - ADMIN_PASSWORD=change_me_later
      - ADMIN_EMAIL=your_email@email.com
    depends_on:
      - db
volumes:
  pg-data:
```

## Snapshot
Snapshot is supported by passing a query param `?snapshot=your_any_key_or_build_number` to the localizedkeystrings request.


## Recommendation and Automation:
With using `CI` and `Fastlane`, create a script or use `fastlane actions localizr` to download and update all the localization strings before `gym` method, So we can always make sure that all strings are updated. 


## TODO:

- [x] iOS format support
- [x] Android format support
- [x] Import/Export contents via CSV file
- [x] CI
- [x] Test cases
- [x] Docker container support.
- [x] Snapshot support.
- [ ] Interactive UI.
- [ ] Able to use google translate for some missing translations.


## Author

Michael Henry Pantaleon, me@iamkel.net

## License

Localizr is available under the MIT license. See the LICENSE file for more info.
