import pytest
from delfino.constants import PackageManager
from delfino.models.pyproject_toml import PyprojectToml

from delfino_docker import _get_python_version_from_pyproject


class TestGetPythonVersionFromPyproject:
    """Test cases for _get_python_version_from_pyproject function."""

    def test_should_extract_python_version_from_requires_python(self) -> None:
        # GIVEN python version is set in projects requires-python
        pyproject_toml = PyprojectToml(
            **{
                "project": {
                    "name": "test-project",
                    "version": "1.0.0",
                    "requires-python": "==3.10.0",
                }
            }
        )

        # WHEN getting python version from pyproject
        result = _get_python_version_from_pyproject(pyproject_toml, PackageManager.UV)

        # THEN the correct version should be returned
        assert result == "3.10.0"

    def test_should_extract_python_version_from_poetry_dependencies_when_requires_python_missing(
        self,
    ) -> None:
        # GIVEN python version is set in poetry dependencies
        pyproject_toml = PyprojectToml(
            **{
                "project": {
                    "name": "test-project",
                    "version": "1.0.0",
                },
                "tool": {
                    "poetry": {
                        "name": "test-project",
                        "version": "1.0.0",
                        "dependencies": {
                            "python": "==3.10.0",
                            "requests": "^2.28.0",
                        },
                    }
                },
            }
        )

        # WHEN getting python version from pyproject with poetry package manager
        result = _get_python_version_from_pyproject(pyproject_toml, PackageManager.POETRY)

        # THEN the version from poetry dependencies should be returned
        assert result == "3.10.0"

    @pytest.mark.parametrize(
        "python_version,expected",
        [
            pytest.param(">=3.10.0", "3.10.0", id=">= specifier"),
            pytest.param(">=3.10.0,<4.0", "3.10.0", id="range specifiers"),
            pytest.param("~3.10.0", "3.10.0", id="~ specifier"),
            pytest.param("^3.10.0", "3.10.0", id="^ specifier"),
            pytest.param("==3.12.0", "3.12.0", id="== specifier"),
            pytest.param("3.11.5", "3.11.5", id="no specifier"),
            pytest.param("!=3.11.0", "3.11.0", id="!= specifier"),
            pytest.param(">=3.10.0,<4.0,!=3.11.0", "3.10.0", id="complex specifier"),
            pytest.param("  >=3.10.0  ", "3.10.0", id="whitespace around specifier"),
        ],
    )
    def test_should_extract_python_version_with_different_specifiers(self, python_version: str, expected: str) -> None:
        # GIVEN there is Python version with different specifiers in requires-python
        pyproject_toml = PyprojectToml(
            **{
                "project": {
                    "name": "test-project",
                    "version": "1.0.0",
                    "requires-python": python_version,
                }
            }
        )

        # WHEN getting python version from pyproject
        result = _get_python_version_from_pyproject(pyproject_toml, PackageManager.UV)

        # THEN the correct version should be returned
        assert result == expected

    def test_should_prefer_requires_python_over_poetry_dependencies(self) -> None:
        # GIVEN a pyproject.toml with both requires-python and poetry python dependencies
        pyproject_data = {
            "project": {
                "name": "test-project",
                "version": "1.0.0",
                "requires-python": ">=3.12.0",
            },
            "tool": {
                "poetry": {
                    "name": "test-project",
                    "version": "1.0.0",
                    "dependencies": {
                        "python": ">=3.10.0,<4.0",
                    },
                }
            },
        }
        pyproject_toml = PyprojectToml(**pyproject_data)

        # WHEN getting python version from pyproject with poetry package manager
        result = _get_python_version_from_pyproject(pyproject_toml, PackageManager.POETRY)

        # THEN requires-python should take precedence
        assert result == "3.12.0"

    def test_should_raise_error_when_python_version_is_missing(self) -> None:
        # GIVEN a pyproject.toml without python version information
        pyproject_toml = PyprojectToml(
            **{
                "project": {
                    "name": "test-project",
                    "version": "1.0.0",
                }
            }
        )

        # WHEN getting python version from pyproject
        # THEN an assertion error should be raised
        with pytest.raises(AssertionError, match="Python version is not set in pyproject.toml"):
            _get_python_version_from_pyproject(pyproject_toml, PackageManager.UV)

    def test_should_raise_error_when_poetry_dependencies_python_is_missing(self) -> None:
        # GIVEN a pyproject.toml with poetry configuration but no python dependency
        pyproject_toml = PyprojectToml(
            **{
                "project": {
                    "name": "test-project",
                    "version": "1.0.0",
                },
                "tool": {
                    "poetry": {
                        "name": "test-project",
                        "version": "1.0.0",
                        "dependencies": {
                            "requests": "^2.28.0",
                        },
                    }
                },
            }
        )

        # WHEN getting python version from pyproject with poetry package manager
        # THEN an assertion error should be raised
        with pytest.raises(AssertionError, match="Python version is not set in pyproject.toml"):
            _get_python_version_from_pyproject(pyproject_toml, PackageManager.POETRY)

    def test_should_raise_error_when_poetry_tool_section_is_missing(self) -> None:
        # GIVEN a pyproject.toml without poetry tool section
        pyproject_toml = PyprojectToml(
            **{
                "project": {
                    "name": "test-project",
                    "version": "1.0.0",
                }
            }
        )

        # WHEN getting python version from pyproject with poetry package manager
        # THEN an assertion error should be raised
        with pytest.raises(AssertionError, match="Python version is not set in pyproject.toml"):
            _get_python_version_from_pyproject(pyproject_toml, PackageManager.POETRY)

    def test_should_handle_empty_poetry_dependencies(self) -> None:
        # GIVEN a pyproject.toml with empty poetry dependencies
        pyproject_data = {
            "project": {
                "name": "test-project",
                "version": "1.0.0",
            },
            "tool": {"poetry": {"name": "test-project", "version": "1.0.0", "dependencies": {}}},
        }
        pyproject_toml = PyprojectToml(**pyproject_data)

        # WHEN getting python version from pyproject with poetry package manager
        # THEN an assertion error should be raised
        with pytest.raises(AssertionError, match="Python version is not set in pyproject.toml"):
            _get_python_version_from_pyproject(pyproject_toml, PackageManager.POETRY)
