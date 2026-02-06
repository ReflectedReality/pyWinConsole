from pyWinConsole import Console, ConsoleBackground, ConsoleFontStyle, ConsoleForeground

Console.clear()

# console title and global style configuration
# setting background color will fill the whole console
Console.configure_console(title = "Cool lib", foreground= ConsoleForeground.WHITE, background= ConsoleBackground.BRIGHT_BLUE)

Console.write("Without ")
Console.write("line ")
Console.write("break ")
Console.write("and ")
Console.write("with ")
Console.write("global ")
Console.write("styles")

Console.write_line() # just empty line

# setting temporary foreground and background, to reset to configuration call Console.reset_colors()
Console.set_text_color(foreground= ConsoleForeground.BLACK, background= ConsoleBackground.WHITE)
for x in range(1, 10):
    Console.write(f"{x}_")

Console.reset_colors()
    
# with positioning
Console.write("_W_", foreground = ConsoleForeground.BLUE, background = ConsoleBackground.BRIGHT_RED, x = 10, y = 3)
Console.write("_O_", style = ConsoleFontStyle.UNDERLINE,  foreground=ConsoleForeground.RED, background=ConsoleBackground.BLACK, x = 13, y = 4)

# another positioning approach
Console.set_cursor_position(x = 16, y = 2)
Console.write("_R_",foreground = ConsoleForeground.BLACK, background = ConsoleBackground.BLUE)
Console.set_cursor_position(x = 19, y = 3)
Console.write("_D_", foreground = ConsoleForeground.BRIGHT_MAGENTA, background = ConsoleBackground.CYAN)

# with line break
Console.write_line() # <- empty line
Console.write_line("some_word")
Console.write_line("some_word", ConsoleFontStyle.BOLD)
Console.write_line("some_word", ConsoleFontStyle.UNDERLINE, ConsoleForeground.BRIGHT_WHITE)
Console.write_line("some_word", ConsoleFontStyle.BOLD, ConsoleForeground.BLUE, ConsoleBackground.BRIGHT_RED)
Console.write_line("some_word", style = "", foreground = ConsoleForeground.BRIGHT_RED, background = ConsoleBackground.BRIGHT_GREEN, x = 20, y = 8)
Console.write_line("some_word", ConsoleFontStyle.NONE, ConsoleForeground.BRIGHT_WHITE, ConsoleBackground.BLACK, 25, 4)
Console.set_cursor_position(x = 0, y = 12)

Console.hide_cursor()
Console.show_cursor()
