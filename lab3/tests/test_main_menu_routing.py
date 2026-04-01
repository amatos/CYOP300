from unittest.mock import Mock

import lab3.lab3main as main_mod


def test_main_menu_routes_to_display_states(monkeypatch, dummy_states):
    called = []

    monkeypatch.setattr(
        main_mod, "Prompt", Mock(indexed_menu=staticmethod(lambda options: 0))
    )
    monkeypatch.setattr(
        main_mod, "display_states", lambda states: called.append("display")
    )
    main_mod.main_menu(dummy_states)
    assert called == ["display"]


def test_main_menu_routes_to_exit(monkeypatch, dummy_states):
    monkeypatch.setattr(
        main_mod, "Prompt", Mock(indexed_menu=staticmethod(lambda options: 4))
    )
    monkeypatch.setattr(
        main_mod, "exit_program", lambda: (_ for _ in ()).throw(SystemExit(0))
    )

    try:
        main_mod.main_menu(dummy_states)
        assert False, "Expected SystemExit"
    except SystemExit:
        assert True
