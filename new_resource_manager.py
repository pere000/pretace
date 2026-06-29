"""
resource_manager.py

TACE Resource Manager

Responsibilities:
- Load resources from config/resources.json
- Validate enabled resources
- Return active resources by type
- Check resource availability
- List enabled resources
- Provide future-compatible interfaces for TACEIntRoute
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================
# LOGGING
# ============================================================

LOGGER_NAME = "tace.resource_manager"

logger = logging.getLogger(LOGGER_NAME)

if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


# ============================================================
# EXCEPTIONS
# ============================================================

class ResourceManagerError(Exception):
    """Base exception for resource manager."""


class ResourceConfigError(ResourceManagerError):
    """Raised when resource configuration is invalid."""


# ============================================================
# RESOURCE MANAGER
# ============================================================

class ResourceManager:
    """
    Manages configured resources for TACE.

    Expected resources.json structure:

    {
        "resources": [
            {
                "name": "ontology",
                "type": "ontology",
                "enabled": true
            },
            {
                "name": "local_ai",
                "type": "local_ai",
                "enabled": true
            }
        ]
    }
    """

    REQUIRED_FIELDS = {
        "name",
        "type",
        "enabled",
    }

    def __init__(self) -> None:
        """
        Initialize ResourceManager.

"""
        self.resources: List[Dict[str, Any]] = []

        self._load_resources()

    # ========================================================
    # LOADING
    # ========================================================


    def _load_resources(self) -> None:
        """
        Load resources from config/tace_runtime.json
        """

        runtime_file = Path(
            "new_tace_runtime.json"
        )

        logger.info(
            "Loading runtime resources from %s",
            runtime_file
        )

        if not runtime_file.exists():

            raise ResourceConfigError(
                f"Runtime configuration not found: {runtime_file}"
            )

        try:

            data = json.load(
                open(
                    runtime_file,
                    "r",
                    encoding="utf-8"
                )
            )

        except Exception as exc:

            raise ResourceConfigError(
                f"Invalid JSON in {runtime_file}"
            ) from exc

        runtime_resources = data.get(
            "resources",
            {}
        )

        resources = []

        for name, enabled in runtime_resources.items():

            resources.append(
                {
                    "name": name,
                    "type": name,
                    "enabled": bool(enabled)
                }
            )

        self.resources = resources

        self.validate_resources()

        logger.info(
            "Loaded %d runtime resources",
            len(self.resources)
        )

    # ========================================================
    # VALIDATION
    # ========================================================

    def validate_resources(self) -> bool:
        """
        Validate all configured resources.

        Returns:
            True if validation succeeds.

        Raises:
            ResourceConfigError
        """
        seen_names = set()

        for resource in self.resources:

            if not isinstance(resource, dict):
                raise ResourceConfigError(
                    "Each resource must be an object"
                )

            missing = self.REQUIRED_FIELDS - resource.keys()

            if missing:
                raise ResourceConfigError(
                    f"Missing required fields: {sorted(missing)}"
                )

            name = resource["name"]

            if name in seen_names:
                raise ResourceConfigError(
                    f"Duplicate resource name: {name}"
                )

            seen_names.add(name)

            if not isinstance(resource["enabled"], bool):
                raise ResourceConfigError(
                    f"'enabled' must be boolean for resource '{name}'"
                )

        logger.info("Resource validation successful")

        return True

    # ========================================================
    # ACCESSORS
    # ========================================================

    def get_all_resources(self) -> List[Dict[str, Any]]:
        """
        Return all configured resources.

        Returns:
            List of resource dictionaries.
        """
        return list(self.resources)

    def get_enabled_resources(self) -> List[Dict[str, Any]]:
        """
        Return all enabled resources.

        Returns:
            Enabled resources.
        """
        return [
            r
            for r in self.resources
            if r.get("enabled", False)
        ]

    def get_resource_by_name(
        self,
        name: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Find resource by name.

        Args:
            name:
                Resource name.

        Returns:
            Resource dict or None.
        """
        for resource in self.resources:
            if resource.get("name") == name:
                return resource

        return None

    def get_resources_by_type(
        self,
        resource_type: str,
        enabled_only: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Return resources matching a type.

        Args:
            resource_type:
                Resource category.
            enabled_only:
                Only include enabled resources.

        Returns:
            Matching resources.
        """
        results = []

        for resource in self.resources:

            if resource.get("type") != resource_type:
                continue

            if enabled_only and not resource.get("enabled"):
                continue

            results.append(resource)

        return results

    def get_active_resource(
        self,
        resource_type: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Return the first active resource of a given type.

        Future TACEIntRoute versions may implement
        scoring and ranking logic here.

        Args:
            resource_type:
                Requested resource type.

        Returns:
            Active resource or None.
        """
        resources = self.get_resources_by_type(
            resource_type=resource_type,
            enabled_only=True,
        )

        if not resources:
            logger.warning(
                "No active resource found for type '%s'",
                resource_type,
            )
            return None

        return resources[0]

    # ========================================================
    # AVAILABILITY
    # ========================================================

    def is_resource_enabled(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a resource is enabled.

        Args:
            name:
                Resource name.

        Returns:
            True if enabled.
        """
        resource = self.get_resource_by_name(name)

        if resource is None:
            return False

        return bool(resource.get("enabled"))

    def check_resource_availability(
        self,
        name: str,
    ) -> bool:
        """
        Check resource availability.

        Current implementation:
        - resource exists
        - resource enabled

        Future versions may include:
        - API ping
        - endpoint checks
        - local model health checks
        - authentication checks

        Args:
            name:
                Resource name.

        Returns:
            Availability status.
        """
        resource = self.get_resource_by_name(name)

        if resource is None:
            logger.warning(
                "Resource '%s' not found",
                name,
            )
            return False

        available = bool(resource.get("enabled"))

        logger.info(
            "Availability check: %s -> %s",
            name,
            available,
        )

        return available

    # ========================================================
    # TACEINTROUTE COMPATIBILITY
    # ========================================================

    def get_candidate_resources(
        self,
        resource_type: str,
    ) -> List[Dict[str, Any]]:
        """
        Future-compatible method for TACEIntRoute.

        Returns candidate resources that may
        later be ranked by routing logic.

        Args:
            resource_type:
                Desired resource type.

        Returns:
            Candidate resource list.
        """
        return self.get_resources_by_type(
            resource_type=resource_type,
            enabled_only=True,
        )

    def reload(self) -> None:
        """
        Reload resource configuration.
        """
        logger.info("Reloading resource configuration")
        self._load_resources()


# ============================================================
# MAIN TEST
# ============================================================

def main() -> None:
    """
    Simple standalone test runner.
    """

    try:
        manager = ResourceManager()

        print("\n=== ENABLED RESOURCES ===")
        for resource in manager.get_enabled_resources():
            print(resource)

        print("\n=== RESOURCE TYPES ===")
        resource_types = sorted(
            {
                r["type"]
                for r in manager.get_enabled_resources()
            }
        )

        for resource_type in resource_types:
            active = manager.get_active_resource(resource_type)
            print(f"{resource_type}: {active}")

        print("\n=== AVAILABILITY ===")
        for resource in manager.get_enabled_resources():
            name = resource["name"]
            print(
                f"{name}: "
                f"{manager.check_resource_availability(name)}"
            )

    except Exception as exc:
        logger.exception("Resource manager test failed")
        print(f"ERROR: {exc}")


if __name__ == "__main__":
    main()
