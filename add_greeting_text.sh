curl -X DELETE -H "Content-Type: application/json" -d '{
  "setting_type":"greeting"
}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=<fb_page_access_token>"

curl -X POST -H "Content-Type: application/json" -d '{
  "setting_type":"greeting",
  "greeting":{
    "text":"Hi {{user_first_name}}! Tap Get Started below to start the conversation."
  }
}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=<fb_page_access_token>"
