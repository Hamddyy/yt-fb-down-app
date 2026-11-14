import os
import threading

import flet as ft
from yt_dlp import YoutubeDL


def get_download_path():
    """يحاول مجلد Download العام، وإن فشل يستخدم مجلد التطبيق."""
    public = "/storage/emulated/0/Download"
    try:
        os.makedirs(public, exist_ok=True)
        test = os.path.join(public, ".w_test")
        with open(test, "w") as f:
            f.write("1")
        os.remove(test)
        return public
    except Exception:
        base = os.getenv("FLET_APP_STORAGE_DATA") or os.path.expanduser("~")
        path = os.path.join(base, "downloads")
        os.makedirs(path, exist_ok=True)
        return path


def main(page: ft.Page):
    page.title = "مدير التحميلات"
    page.rtl = True
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 16

    query = ft.TextField(label="اسم الفيديو/الأغنية أو الرابط", expand=True)
    fmt = ft.Dropdown(
        label="الصيغة",
        value="video",
        options=[
            ft.dropdown.Option("video", "فيديو (MP4)"),
            ft.dropdown.Option("audio", "صوت (M4A)"),
        ],
    )
    status = ft.Text("")
    progress = ft.ProgressBar(visible=False)
    results = ft.Column()
    state = {"limit": 10, "q": ""}

    def set_status(msg):
        status.value = msg
        page.update()

    def hook(d):
        if d["status"] == "downloading":
            p = (d.get("_percent_str") or "").strip()
            s = (d.get("_speed_str") or "").strip()
            status.value = f"⏳ {p}  {s}"
            page.update()
        elif d["status"] == "finished":
            status.value = "✅ اكتمل التحميل، جاري الحفظ..."
            page.update()

    def download(url):
        folder = get_download_path()
        opts = {"progress_hooks": [hook], "quiet": True, "noplaylist": True}
        if fmt.value == "audio":
            opts["format"] = "bestaudio[ext=m4a]/bestaudio/best"
            opts["outtmpl"] = os.path.join(folder, "audio_%(id)s.%(ext)s")
        else:
            opts["format"] = "best[height<=480][ext=mp4]/best[ext=mp4]/best"
            opts["outtmpl"] = os.path.join(folder, "video_%(id)s.%(ext)s")

        def run():
            progress.visible = True
            set_status("🚀 جاري بدء التحميل...")
            try:
                with YoutubeDL(opts) as ydl:
                    ydl.extract_info(url, download=True)
                set_status(f"🎉 تم الحفظ في:\n{folder}")
            except Exception as e:
                set_status(f"❌ خطأ: {e}")
            progress.visible = False
            page.update()

        threading.Thread(target=run, daemon=True).start()

    def show_results(entries):
        results.controls.clear()
        for i, e in enumerate(entries, 1):
            dur = e.get("duration")
            dur_s = f"{int(dur)//60}:{int(dur)%60:02d}" if dur else "؟"
            url = e.get("url") or e.get("webpage_url")
            results.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{i}. {e.get('title', 'بدون عنوان')}"),
                    subtitle=ft.Text(f"⏱️ {dur_s}"),
                    trailing=ft.Icon(ft.Icons.DOWNLOAD),
                    on_click=lambda _, u=url: download(u),
                )
            )
        if state["limit"] < 30:
            results.controls.append(
                ft.TextButton("عرض 10 نتائج إضافية", on_click=more)
            )
        page.update()

    def search():
        def run():
            progress.visible = True
            set_status(f'🔍 جاري البحث عن "{state["q"]}"...')
            try:
                with YoutubeDL({"extract_flat": True, "quiet": True}) as ydl:
                    info = ydl.extract_info(
                        f"ytsearch{state['limit']}:{state['q']}", download=False
                    )
                entries = info.get("entries", [])
                if not entries:
                    set_status("❌ لا توجد نتائج")
                else:
                    set_status("اختر فيديو للتحميل 👇")
                    show_results(entries)
            except Exception as e:
                set_status(f"❌ خطأ في البحث: {e}")
            progress.visible = False
            page.update()

        threading.Thread(target=run, daemon=True).start()

    def more(_):
        state["limit"] = min(state["limit"] + 10, 30)
        search()

    def go(_):
        text = (query.value or "").strip()
        if not text:
            set_status("⚠️ اكتب اسماً أو الصق رابطاً")
            return
        results.controls.clear()
        if text.startswith("http"):
            download(text)
        else:
            state["q"] = text
            state["limit"] = 10
            search()

    page.add(
        ft.Text("مدير تحميلات يوتيوب وفيسبوك", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([query]),
        fmt,
        ft.ElevatedButton("بحث / تحميل", icon=ft.Icons.SEARCH, on_click=go),
        progress,
        status,
        results,
    )


ft.app(target=main)
