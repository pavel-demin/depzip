import depzip

depzip.bundle(
    modules=[
        "matplotlib.backends.backend_qtagg",
        "matplotlib.figure",
        "matplotlib.style",
        "matplotlib",
        "numpy",
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtNetwork",
        "PySide6.QtUiTools",
        "PySide6.QtWidgets",
    ],
    includes=[
        "Lib\\site-packages\\depzip\\import.exe",
        "Lib\\site-packages\\matplotlib\\mpl-data",
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
