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

"""Implementation of the 'aea login' subcommand."""

import click

from aea.cli.common import _update_cli_config
from aea.cli.registry.settings import AUTH_TOKEN_KEY
from aea.cli.registry.utils import registry_login


@click.command(name="login", help="Login to Registry account")
@click.argument("username", type=str, required=True)
@click.option("--password", type=str, required=True, prompt=True, hide_input=True)
def login(username, password):
    """Login to Registry account."""
    click.echo("Signing in as {}...".format(username))
    token = registry_login(username, password)
    _update_cli_config({AUTH_TOKEN_KEY: token})
    click.echo("Successfully signed in: {}.".format(username))
