"""Tests for dino_game asset manifest helpers."""

import ast
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DINO_GAME_PATH = PROJECT_ROOT / "dino_game.py"


def load_asset_manifest_helpers():
    source = DINO_GAME_PATH.read_text(encoding="utf-8")
    module = ast.parse(source, filename=str(DINO_GAME_PATH))
    helper_names = {
        "get_required_image_asset_paths",
        "iter_required_image_asset_paths",
        "find_missing_required_image_assets",
        "load_required_game_images",
    }
    selected_nodes = []
    for node in module.body:
        if isinstance(node, ast.ImportFrom) and node.module == "pathlib":
            selected_nodes.append(node)
        if isinstance(node, ast.FunctionDef) and node.name in helper_names:
            selected_nodes.append(node)
    helper_module = ast.Module(body=selected_nodes, type_ignores=[])
    namespace = {}
    exec(compile(helper_module, str(DINO_GAME_PATH), "exec"), namespace)
    return namespace


HELPERS = load_asset_manifest_helpers()
get_required_image_asset_paths = HELPERS["get_required_image_asset_paths"]
iter_required_image_asset_paths = HELPERS["iter_required_image_asset_paths"]
find_missing_required_image_assets = HELPERS["find_missing_required_image_assets"]
load_required_game_images = HELPERS["load_required_game_images"]


class TestGameAssets(unittest.TestCase):
    """Validate the centralized required image asset manifest."""

    def test_required_image_asset_exists(self):
        """Every required image path used by the game must exist on disk."""
        for relative_path in sorted(set(iter_required_image_asset_paths())):
            with self.subTest(relative_path=relative_path):
                self.assertTrue((PROJECT_ROOT / relative_path).exists(), relative_path)

    def test_find_missing_required_image_assets_returns_no_missing_paths(self):
        """The manifest should resolve cleanly against the current repository."""
        self.assertEqual(find_missing_required_image_assets(PROJECT_ROOT), [])

    def test_load_required_game_images_uses_manifest_paths(self):
        """Loading should be driven by the central manifest instead of ad hoc globals."""
        loaded_paths = []
        rotated = []

        def fake_load_image(path):
            loaded_paths.append(path)
            return f"loaded:{path}"

        def fake_rotate(image, angle):
            rotated.append((image, angle))
            return (image, angle)

        images = load_required_game_images(fake_load_image, fake_rotate)
        manifest = get_required_image_asset_paths()

        expected_loaded_paths = []
        for value in manifest.values():
            if isinstance(value, str):
                expected_loaded_paths.append(value)
            else:
                expected_loaded_paths.extend(value)

        self.assertEqual(loaded_paths, expected_loaded_paths)
        self.assertEqual(
            rotated,
            [
                (images["DINO_OOPS_IMG"], -90),
                (images["ROADRUNNER_OOPS_IMG"], -90),
            ],
        )
        self.assertEqual(images["DINO_IMG"], f"loaded:{manifest['DINO_IMG']}")
        self.assertEqual(images["COWBOY_IMG"], f"loaded:{manifest['COWBOY_IMG']}")
        self.assertEqual(images["ROADRUNNER_IMG"], f"loaded:{manifest['ROADRUNNER_IMG']}")


if __name__ == "__main__":
    unittest.main()
