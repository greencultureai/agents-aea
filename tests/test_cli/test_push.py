# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------
"""Test module for Registry push methods."""

from unittest import TestCase, mock

from click import ClickException
from click.testing import CliRunner

from aea.cli import cli
from aea.cli.push import _check_package_public_id, _save_item_locally

from tests.conftest import CLI_LOG_OPTION
from tests.test_cli.tools_for_testing import ContextMock, PublicIdMock

from ..conftest import AUTHOR


@mock.patch("aea.cli.push.copytree")
class SaveItemLocallyTestCase(TestCase):
    """Test case for save_item_locally method."""

    @mock.patch(
        "aea.cli.push._try_get_vendorized_item_target_path", return_value="target"
    )
    @mock.patch("aea.cli.push._try_get_item_source_path", return_value="source")
    @mock.patch("aea.cli.push._check_package_public_id", return_value=None)
    def test_save_item_locally_positive(
        self,
        _check_package_public_id_mock,
        _try_get_item_source_path_mock,
        _try_get_vendorized_item_target_path_mock,
        copy_tree_mock,
    ):
        """Test for save_item_locally positive result."""
        item_type = "skill"
        item_id = PublicIdMock()
        ctx_mock = ContextMock()
        _save_item_locally(ctx_mock, item_type, item_id)
        _try_get_item_source_path_mock.assert_called_once_with(
            "cwd", item_id.author, "skills", item_id.name
        )
        _try_get_vendorized_item_target_path_mock.assert_called_once_with(
            ctx_mock.agent_config.registry_path,
            item_id.author,
            item_type + "s",
            item_id.name,
        )
        _check_package_public_id_mock.assert_called_once_with(
            "source", item_type, item_id
        )
        copy_tree_mock.assert_called_once_with("source", "target")


@mock.patch(
    "aea.cli.push._load_yaml",
    return_value={"author": AUTHOR, "name": "name", "version": "0.1.0"},
)
class CheckPackagePublicIdTestCase(TestCase):
    """Test case for _check_package_public_id method."""

    def test__check_package_public_id_positive(self, *mocks):
        """Test for _check_package_public_id positive result."""
        _check_package_public_id(
            "source-path",
            "item-type",
            PublicIdMock.from_str("{}/name:0.1.0".format(AUTHOR)),
        )

    def test__check_package_public_id_negative(self, *mocks):
        """Test for _check_package_public_id negative result."""
        with self.assertRaises(ClickException):
            _check_package_public_id(
                "source-path",
                "item-type",
                PublicIdMock.from_str("{}/name:0.1.1".format(AUTHOR)),
            )


class TestPushLocalFailsArgumentNotPublicId:
    """Test the case when we try a local push with a non public id."""

    @classmethod
    def setup_class(cls):
        """Set the tests up."""
        cls.runner = CliRunner()
        cls.result = cls.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "push", "--local", "connection", "oef"],
            standalone_mode=False,
        )

    def test_exit_code_2(self):
        """Test the exit code is 2 (i.e. bad usage)."""
        assert self.result.exit_code == 1
        assert self.result.exception.exit_code == 2

    @classmethod
    def teardown_class(cls):
        """Tear the tests down."""


@mock.patch("aea.cli.push.try_to_load_agent_config")
@mock.patch("aea.cli.push._save_item_locally")
@mock.patch("aea.cli.push.push_item")
class PushCommandTestCase(TestCase):
    """Test case for CLI push command."""

    def setUp(self):
        """Set it up."""
        self.runner = CliRunner()

    def test_push_connection_positive(self, *mocks):
        """Test for CLI push connection positive result."""
        self.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "push", "--registry", "connection", "author/name:0.1.0"],
            standalone_mode=False,
        )
        self.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "push", "connection", "author/name:0.1.0"],
            standalone_mode=False,
        )

    def test_push_protocol_positive(self, *mocks):
        """Test for CLI push protocol positive result."""
        self.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "push", "--registry", "protocol", "author/name:0.1.0"],
            standalone_mode=False,
        )
        self.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "push", "protocol", "author/name:0.1.0"],
            standalone_mode=False,
        )

    def test_push_skill_positive(self, *mocks):
        """Test for CLI push skill positive result."""
        self.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "push", "--registry", "skill", "author/name:0.1.0"],
            standalone_mode=False,
        )
        self.runner.invoke(
            cli,
            [*CLI_LOG_OPTION, "push", "skill", "author/name:0.1.0"],
            standalone_mode=False,
        )
