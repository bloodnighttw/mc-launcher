import os
import sys
import shutil
import winreg
import ctypes


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def install_fonts(font_paths):
    font_dir = os.path.join(os.environ["WINDIR"], "Fonts")

    for font_path in font_paths:
        font_name = os.path.basename(font_path)
        dest_path = os.path.join(font_dir, font_name)

        # Copy the font file to the Fonts directory
        shutil.copy(font_path, dest_path)

        # Register the font in the Windows registry
        font_name_without_ext = os.path.splitext(font_name)[0]
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts",
            0,
            winreg.KEY_SET_VALUE,
        ) as key:
            winreg.SetValueEx(key, font_name_without_ext, 0, winreg.REG_SZ, font_name)

    os.system("gpupdate /force")


if __name__ == "__main__":

    """
    I edited 'MinecraftTen-VGORe.ttf' to 'MinecraftTen-Regular.otf' on
    'MinecraftTen-VGORe.ttf' to change the metadata to overcome name
    repitition between different module
    """
    font_paths = [
        "ui/font/minecraft-ten-font/MinecraftTen-Regular.otf",
        "ui/font/minecraft-font/MinecraftBold-nMK1.otf",
        "ui/font/minecraft-font/MinecraftItalic-R8Mo.otf",
        "ui/font/minecraft-font/MinecraftItalic-R8Mo.otf",
        "ui/font/minecraft-font/MinecraftRegular-Bmg3.otf",
    ]

    if is_admin():
        install_fonts(font_paths)
    else:
        # Re-run the script with admin privileges
        script_path = os.path.abspath(__file__)
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, script_path, None, 1
        )
