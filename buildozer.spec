[app]

# (str) Title of your application
title = YouTube & Facebook Downloader

# (str) Package name
package.name = ytdownloader

# (str) Package domain (needed for android packaging)
package.domain = org.downloader

# (str) Source directory where the application files are located
source.dir = .

# (str) Application versioning
version = 0.1

# (list) Source files to include (let it match python files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Source files to exclude (optional)
source.exclude_exts = spec

# (list) List of directory to include
source.include_dirs = 

# (list) List of exclusions
source.exclude_dirs = tests bin

# (list) Application requirements
requirements = python3,requests,yt-dlp,certifi,urllib3,idna,charset-normalizer

# (str) Supported orientations (landscape, sensor, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (str) Supported API level (recommended to use latest stable)
android.api = 33

# (int) Minimum API level your app supports
android.minapi = 21

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with color))
log_level = 2

# (int) Display warning if buildroot is in home directory (0 = False, 1 = DANGER)
warn_on_root = 1
