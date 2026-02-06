import ctypes
from dataclasses import dataclass
import os

#--------- Console decor ---------#
@dataclass(frozen=True)
class ConsoleForeground:
    BLACK   = 0
    BLUE    = 0x1
    GREEN   = 0x2
    RED     = 0x4
    CYAN    = BLUE | GREEN
    MAGENTA = RED | BLUE
    YELLOW  = RED | GREEN
    WHITE   = RED | GREEN | BLUE

    BRIGHT_BLUE    = BLUE | 0x8
    BRIGHT_GREEN   = GREEN | 0x8
    BRIGHT_RED     = RED | 0x8
    BRIGHT_CYAN    = CYAN | 0x8
    BRIGHT_MAGENTA = MAGENTA | 0x8
    BRIGHT_YELLOW  = YELLOW | 0x8
    BRIGHT_WHITE   = WHITE | 0x8

@dataclass(frozen=True)
class ConsoleBackground:
    BLACK   = 0
    BLUE    = 0x10
    GREEN   = 0x20
    RED     = 0x40
    CYAN    = BLUE | GREEN
    MAGENTA = RED | BLUE
    YELLOW  = RED | GREEN
    WHITE   = RED | GREEN | BLUE

    BRIGHT_BLUE    = BLUE | 0x80
    BRIGHT_GREEN   = GREEN | 0x80
    BRIGHT_RED     = RED | 0x80
    BRIGHT_CYAN    = CYAN | 0x80
    BRIGHT_MAGENTA = MAGENTA | 0x80
    BRIGHT_YELLOW  = YELLOW | 0x80
    BRIGHT_WHITE   = WHITE | 0x80

@dataclass(frozen=True)
class ConsoleFontStyle:
    NONE = ""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


#--------- C-type tructures ---------#
 
class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class CONSOLE_CURSOR_INFO(ctypes.Structure):
    _fields_ = [("dwSize", ctypes.c_int),
                ("bVisible", ctypes.c_bool)]
    
class SMALL_RECT(ctypes.Structure):
    _fields_ = [("Left", ctypes.c_short),
                ("Top", ctypes.c_short),
                ("Right", ctypes.c_short),
                ("Bottom", ctypes.c_short)]

class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", ctypes.c_ushort),
        ("srWindow", SMALL_RECT),
        ("dwMaximumWindowSize", COORD)
    ]

#--------- Console ---------#
#   Simple WinAPI wrapper   # 
#---------------------------#

@dataclass
class Config:
    CONSOLE_TITLE = "MyApp"
    GLOBAL_FOREGROUND = ConsoleForeground.WHITE
    GLOBAL_BACKGROUND = ConsoleBackground.BLACK


class Console:
    CONFIG = Config()

    CURRENT_TEXT_FOREGROUND: int | None = None
    CURRENT_TEXT_BACKGROUND: int | None = None

    STD_OUTPUT_HANDLE = -11
    h = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    @staticmethod
    def configure_console(title = "MyApp", foreground: int = ConsoleForeground.WHITE, background: int = ConsoleBackground.BLACK):
        Console.CONFIG.CONSOLE_TITLE = title
        Console.CONFIG.GLOBAL_FOREGROUND = foreground
        Console.CONFIG.GLOBAL_BACKGROUND = background

        Console.set_title(title)

        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(Console.h, ctypes.byref(csbi))

        width, height = Console.get_window_size()

        cells = width * height
        attr = foreground | background

        written = ctypes.c_ulong()

        ctypes.windll.kernel32.FillConsoleOutputAttribute(
            Console.h, attr, cells, COORD(0, 0), ctypes.byref(written)
        )
        
    #--------- Cursor Region ---------#

    @staticmethod
    def hide_cursor():
        info = CONSOLE_CURSOR_INFO()
        info.dwSize = 1
        info.bVisible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(Console.h, ctypes.byref(info))

    @staticmethod
    def show_cursor():
        info = CONSOLE_CURSOR_INFO()
        info.dwSize = 1
        info.bVisible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(Console.h, ctypes.byref(info))

    @staticmethod
    def set_cursor_position(x: int, y: int):
        pos = COORD(x, y)
        ctypes.windll.kernel32.SetConsoleCursorPosition(Console.h, pos)
    

    #--------- Color Region ---------#

    @staticmethod
    def set_text_color(foreground: int | None = None, background: int | None = None):
        if foreground is None:
            if Console.CURRENT_TEXT_FOREGROUND is None:
                foreground = Console.CONFIG.GLOBAL_FOREGROUND
            else:
                foreground = Console.CURRENT_TEXT_FOREGROUND
        else:
            Console.CURRENT_TEXT_FOREGROUND = foreground

        if background is None:
            if Console.CURRENT_TEXT_BACKGROUND is None:
                background = Console.CONFIG.GLOBAL_BACKGROUND
            else:
                background = Console.CURRENT_TEXT_BACKGROUND
        else:
            Console.CURRENT_TEXT_BACKGROUND = background

        ctypes.windll.kernel32.SetConsoleTextAttribute(Console.h, foreground | background)

    @staticmethod
    def reset_colors(): 
        Console.CURRENT_TEXT_FOREGROUND = None
        Console.CURRENT_TEXT_BACKGROUND = None

        Console.set_text_color()

    #--------- Output Region ---------#
    
    @staticmethod
    def write(text: str = "", style: str | None = None,
                  foreground: int | None = None, background: int | None = None,
                  x: int = None, y: int = None):
        
        if style is None:
            styled_text = text
        else:
            styled_text = f"{style}{text}{ConsoleFontStyle.RESET}"

        if x is not None and y is not None:
            Console.set_cursor_position(x, y)

        Console.set_text_color(foreground, background)
        print(styled_text, end="", flush=True)

    def write_line(text: str = "", style: str | None = None, 
                    foreground: int | None = None, background: int | None = None,
                    x: int = None, y: int = None):
        
        Console.write(text + "\n", style, foreground, background, x, y)

    @staticmethod
    def clear():
        os.system("cls")
    
    #--------- Util Region ---------#

    @staticmethod
    def set_title(title):
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    
    @staticmethod
    def get_window_size():
        csbi = CONSOLE_SCREEN_BUFFER_INFO()
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(Console.h, ctypes.byref(csbi))
        width = csbi.srWindow.Right - csbi.srWindow.Left + 1
        height = csbi.srWindow.Bottom - csbi.srWindow.Top + 1

        return width, height



