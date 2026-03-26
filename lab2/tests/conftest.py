import sys
import types


class _FakeTerminalMenu:
    def __init__(self, options):
        self.options = options
        self._selected_index = 0

    def show(self):
        return self._selected_index


fake_simple_term_menu = types.ModuleType("simple_term_menu")
fake_simple_term_menu.TerminalMenu = _FakeTerminalMenu
sys.modules.setdefault("simple_term_menu", fake_simple_term_menu)
