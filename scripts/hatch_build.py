"""A Hatchling plugin to build the gosling-widget frontend."""

import os
import pathlib
import subprocess

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

ROOT = pathlib.Path(__file__).parent / ".."


class GoslingWidgetBuildHook(BuildHookInterface):
    """Hatchling plugin to build the gosling widget frontend."""

    PLUGIN_NAME = "gosling-widget"

    def initialize(self, version: str, build_data: dict) -> None:
        """Initialize the plugin."""
        if os.getenv("SKIP_DENO_BUILD", "0") == "1":
            # Skip the build if the environment variable is set
            # Useful in CI/CD pipelines
            return

        if not (ROOT / "gosling/static/widget.js").exists():
            subprocess.check_call(["deno", "task", "build"], cwd=ROOT)
