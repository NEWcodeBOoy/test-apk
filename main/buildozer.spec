[app]

title = Flora Daily
package.name = floradaily
package.domain = org.brandon

source.dir = .
source.include_exts = py,png,jpg,json,txt

version = 1.0

requirements = python3,kivy,plyer

orientation = portrait
fullscreen = 0

android.permissions = POST_NOTIFICATIONS,VIBRATE,CALL_PHONE,SEND_SMS

[buildozer]

log_level = 2
warn_on_root = 1
