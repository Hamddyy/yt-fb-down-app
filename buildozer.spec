[app]

# (str) Title of your application
title = YouTube & Facebook Downloader

# (str) Package name
package.name = ytdownloader

# (str) Package domain (needed for android packaging)
package.domain = org.downloader

# (list) Source files to include (let it match python files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (optional)
source.exclude_exts = spec

# (list) List of directory to include
source.include_dirs = 

# (list) List of exclusions
source.exclude_dirs = tests bin

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,requests,yt-dlp,certifi,urllib3,idna,charset-normalizer,idna

# (str) Supported orientations (landscape, sensor, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with color))
log_level = 2

# (int) Display warning if buildroot is in home directory (0 = False, 1 = DANGER)
warn_on_root = 1
