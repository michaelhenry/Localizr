module Fastlane
  module Actions

    class LocalizrAction < Action

      def self.localizr_request(server_url, app_slug, locale_code, auth_token, lproj_target_path, lproj_name)
        lproj_folder = "#{lproj_target_path}/#{lproj_name}.lproj"
        sh "mkdir -p #{lproj_folder}"
        sh "curl --fail --silent -o #{lproj_folder}/Localizable.strings #{server_url}/app/#{app_slug}.#{locale_code}?format=ios -H 'Authorization: Token #{auth_token}'"
      end

      def self.run(params)
        UI.message "Server URL: #{params[:localizr_server]}"
        UI.message "Base Locale code: #{params[:base_locale_code]}"
        UI.message "Locale codes: #{params[:locale_codes]}"
        UI.message "LProj Target path: #{params[:lproj_target_path]}"
        
        params[:locale_codes].split(",").each { |locale_code|
          lproj_name = locale_code.strip
          if locale_code.downcase.strip == params[:base_locale_code].downcase.strip
            lproj_name = 'Base'
          end

          localizr_request(params[:localizr_server], 
            params[:localizr_app_slug], 
            locale_code, 
            params[:localizr_api_token], 
            params[:lproj_target_path], 
            lproj_name)
        }
      rescue
        UI.user_error!("An error occured on localizr. Please verify the configuration and then try again.")
      end

      #####################################################
      # @!group Documentation
      #####################################################

      def self.description
         "A Localization DSL for IOS and Android."
      end

      def self.details
        "Localizr is a DSL that handles and automates localization files. Basically we give limited access to the translators to let them input or upload different keystrings and we developer will just fetch it on development or deployment only when if there is an update. This will lessen or prevent the mistake that developer made because he/she has no clue what are those words is and most of them (including me, but not all) are just copy pasting those words (especially when it comes to chinese or japanese characters) from excel to the Localizable.strings via Xcode."
      end

      def self.available_options
        [
          FastlaneCore::ConfigItem.new(key: :localizr_server,
                                       env_name: "FL_LOCALIZR_SERVER",
                                       description: "Server URL for LocalizrAction",
                                       verify_block: proc do |value|
                                          UI.user_error!("No Server URL for LocalizrAction given, pass using `localizr_server: 'http://localizr.youdomain.com'`") unless (value and not value.empty?)
                                       end),
          FastlaneCore::ConfigItem.new(key: :localizr_api_token,
                                       env_name: "FL_LOCALIZR_API_TOKEN",
                                       description: "API Token for LocalizrAction",
                                       verify_block: proc do |value|
                                          UI.user_error!("No API token for LocalizrAction given, pass using `localizr_api_token: 'token'`") unless (value and not value.empty?)
                                       end),
          FastlaneCore::ConfigItem.new(key: :localizr_app_slug,
                                       env_name: "FL_LOCALIZR_APP_SLUG",
                                       description: "App slug for LocalizrAction",
                                       verify_block: proc do |value|
                                          UI.user_error!("No App slug for LocalizrAction given, pass using `localizr_app_slug: 'my-app'`") unless (value and not value.empty?)
                                       end),
          FastlaneCore::ConfigItem.new(key: :base_locale_code,
                                       env_name: "FL_LOCALIZR_BASE_LOCALE_CODE",
                                       description: "Base locale code for LocalizrAction",
                                       default_value: 'en'),
          FastlaneCore::ConfigItem.new(key: :locale_codes,
                                       env_name: "FL_LOCALIZR_LOCALE_CODES",
                                       description: "Locale codes for LocalizrAction",
                                       verify_block: proc do |value|
                                          UI.user_error!("No Locale codes for LocalizrAction given, pass using `locale_codes: 'en,ja,pt,zh'") unless (value and not value.empty?)
                                       end),
          FastlaneCore::ConfigItem.new(key: :lproj_target_path,
                                       env_name: "FL_LOCALIZR_LPROJ_TARGET_PATH",
                                       description: "Lproj target path for LocalizrAction",
                                       verify_block: proc do |value|
                                          UI.user_error!("No lproj_target_path for LocalizrAction given, pass using `lproj_target_path: 'Project'") unless (value and not value.empty?)
                                       end),
        ]
      end

      def self.authors
        ["@michaelhenry119","https://github.com/michaelhenry"]
      end

      def self.is_supported?(platform)
        platform == :ios
      end
    end
  end
end