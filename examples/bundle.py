import depzip

depzip.bundle(
    applications=[
        "app",
        "pyside6-uic",
    ],
    modules=[
        "app",
        "PySide6.QtUiTools",
    ],
    includes=[
        "Lib\\site-packages\\matplotlib\\mpl-data",
        "Lib\\site-packages\\numpy.libs",
        "Lib\\site-packages\\pyside6-uic",
        "Lib\\site-packages\\PySide6\\plugins\\platforms\\qwindows.dll",
        "Lib\\site-packages\\PySide6\\plugins\\styles\\qmodernwindowsstyle.dll",
        "Lib\\site-packages\\PySide6\\uic.exe",
    ],
    excludes=[
        "python.exe",
        "pythonw.exe",
    ],
    output="bundle.zip",
)
