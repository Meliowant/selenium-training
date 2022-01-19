import pytest


def id_from_menuitem(test_params):
    title = test_params.get("menu_item").replace(" ", "_")
    return title
