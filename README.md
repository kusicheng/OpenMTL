# OpenMTL
The front end and user-facing application for BackToMTL, an accessible, fast, and lightweight option for complex, mass translation

## Run the desktop prototype

Requires Python 3.10 or newer and PyQt6.

```powershell
python -m pip install -r requirements.txt
python main.py
```

You can also launch it with `python -m openmtl`.

The interface uses a black, white, and gray theme with a fading graph-paper background. The home screen has five rotating greetings and a small Duobird mascot. Set your display name in Settings; after seven days away, the app greets you with “good to see you again.” Use the refresh icon to cycle greetings manually.

- **Auto translate:** choose or drop image, PDF, and text files into a local staging list, select a language pair, and preview the workflow.
- **Translate and edit:** preview a bundled English sample in eight languages, edit the result, and copy it. Custom text translation requires the backend.
- **Settings:** save your display name, default languages, and whether to remember your last language pair.

These are prototype scenes. BackToMTL is not connected, and file previews do not read, translate, upload, or export file contents. Preferences and the last-use time are stored locally with Qt's platform settings.

Keyboard shortcuts: `Ctrl+1` Home, `Ctrl+2` Auto translate, `Ctrl+3` Translate and edit, and `Ctrl+,` Settings.

## Repository boundaries

OpenMTL owns the frontend and user-facing application. [BackToMTL](https://github.com/kusicheng/backtomtl) owns the translation backend, image processing, OCR, detection, rendering, and related training code. [RagMTL](https://github.com/kusicheng/ragmtl) owns MAGRA retrieval and benchmarking.
