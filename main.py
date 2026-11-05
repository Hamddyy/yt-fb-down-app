import os
import subprocess
import sys
from yt_dlp import YoutubeDL


def update_ytdlp():
  print("🔄 جاري التحقق من تحديثات مكتبة التحميل...")
  try:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("✅ المكتبة محدثة لأحدث إصدار وجاهزة للعمل.")
  except Exception:
    print("⚠️ تعذر التحديث التلقائي، سنتابع بالنسخة الحالية.")


def get_download_path():
  path = "/storage/emulated/0/Download"
  if not os.path.exists(path):
    os.makedirs(path)
  return path


def progress_hook(d):
  if d["status"] == "downloading":
    print(
        f"⏳ جاري التحميل: {d.get('_percent_str', '0%')} - السرعة:"
        f" {d.get('_speed_str', 'N/A')}",
        end="\r",
    )
  elif d["status"] == "finished":
    print("\n✅ اكتمل التحميل، جاري المعالجة والحفظ...")


def download_media(url, choice):
  ydl_opts = {
      "progress_hooks": [progress_hook],
  }

  if choice == "1":
    # تحميل فيديو MP4
    ydl_opts.update({
        "format": "best[height<=480][ext=mp4]/best[ext=mp4]/best",
        "outtmpl": os.path.join(get_download_path(), "video_%(id)s.%(ext)s"),
    })
    media_type = "فيديو"
  elif choice == "2":
    # تحميل الصوت بصيغة m4a جاهزة مباشرة (بدون الحاجة إلى FFmpeg للتحويل)
    ydl_opts.update({
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": os.path.join(get_download_path(), "audio_%(id)s.m4a"),
    })
    media_type = "صوت (Audio)"
  else:
    print("❌ اختيار غير صحيح!")
    return

  try:
    print(f"\n🔍 جاري تحليل الرابط واستخراج معلومات الـ {media_type}...")
    with YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(url, download=True)
      file_id = info.get("id", "file")
      ext = "m4a" if choice == "2" else "mp4"
      prefix = "audio" if choice == "2" else "video"
      print(f"\n🎉 تم حفظ الـ {media_type} بنجاح في مجلد Download باسم:")
      print(f"{prefix}_{file_id}.{ext}")
  except Exception as e:
    print(f"\n❌ حدث خطأ أثناء التحميل: {str(e)}")


def main():
  update_ytdlp()

  print("\n=============================================")
  print("   مدير تحميلات يوتيوب وفيسبوك (Pydroid 3)")
  print("=============================================")

  while True:
    print("\n--- القائمة الرئيسية ---")
    print("1. تحميل فيديو (MP4)")
    print("2. تحميل صوت (Audio)")
    print("3. خروج (exit)")

    choice = input("اختر الرقم المناسب (1/2/3): ").strip()

    if choice == "3" or choice.lower() == "exit":
      print("👋 شكراً لاستخدامك البرنامج. إلى اللقاء!")
      break

    if choice not in ["1", "2"]:
      print("⚠️ خيار خاطئ، يرجى إدخال 1 أو 2 أو 3.")
      continue

    url = input(
        "\n🔗 الصق رابط الفيديو (أو اكتب 'exit' للخروج): "
    ).strip()

    if url.lower() == "exit":
      print("👋 شكراً لاستخدامك البرنامج. إلى اللقاء!")
      break

    if not url:
      print("⚠️ يرجى إدخال رابط صحيح!")
      continue

    download_media(url, choice)


if __name__ == "__main__":
  main()
