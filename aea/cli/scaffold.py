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

"""Implementation of the 'aea scaffold' subcommand."""

import os
import shutil
import sys
from pathlib import Path

import click

from jsonschema import ValidationError

from aea import AEA_DIR
from aea.cli.common import (
    Context,
    DEFAULT_VERSION,
    _validate_package_name,
    logger,
    pass_ctx,
    try_to_load_agent_config,
)
from aea.configurations.base import DEFAULT_AEA_CONFIG_FILE, PublicId
from aea.configurations.base import (  # noqa: F401
    DEFAULT_CONNECTION_CONFIG_FILE,
    DEFAULT_PROTOCOL_CONFIG_FILE,
    DEFAULT_SKILL_CONFIG_FILE,
)


@click.group()
@pass_ctx
def scaffold(ctx: Context):
    """Scaffold a resource for the agent."""
    try_to_load_agent_config(ctx)


@scaffold.command()
@click.argument("connection_name", type=str, required=True)
@pass_ctx
def connection(ctx: Context, connection_name: str) -> None:
    """Add a connection scaffolding to the configuration file and agent."""
    _scaffold_item(ctx, "connection", connection_name)


@scaffold.command()
@click.argument("protocol_name", type=str, required=True)
@pass_ctx
def protocol(ctx: Context, protocol_name: str):
    """Add a protocol scaffolding to the configuration file and agent."""
    _scaffold_item(ctx, "protocol", protocol_name)


@scaffold.command()
@click.argument("skill_name", type=str, required=True)
@pass_ctx
def skill(ctx: Context, skill_name: str):
    """Add a skill scaffolding to the configuration file and agent."""
    _scaffold_item(ctx, "skill", skill_name)


def _scaffold_item(ctx: Context, item_type, item_name):
    """Add an item scaffolding to the configuration file and agent."""
    _validate_package_name(item_name)
    author_name = ctx.agent_config.author
    loader = getattr(ctx, "{}_loader".format(item_type))
    default_config_filename = globals()[
        "DEFAULT_{}_CONFIG_FILE".format(item_type.upper())
    ]

    item_type_plural = item_type + "s"
    existing_ids = getattr(ctx.agent_config, "{}s".format(item_type))
    existing_ids_only_author_and_name = map(lambda x: (x.author, x.name), existing_ids)
    # check if we already have an item with the same public id
    if (author_name, item_name) in existing_ids_only_author_and_name:
        logger.error(
            "A {} with name '{}' already exists. Aborting...".format(
                item_type, item_name
            )
        )
        sys.exit(1)

    try:
        agent_name = ctx.agent_config.agent_name
        click.echo(
            "Adding {} scaffold '{}' to the agent '{}'...".format(
                item_type, item_name, agent_name
            )
        )

        # create the item folder
        Path(item_type_plural).mkdir(exist_ok=True)
        dest = Path(os.path.join(item_type_plural, item_name))

        # copy the item package into the agent project.
        src = Path(os.path.join(AEA_DIR, item_type_plural, "scaffold"))
        logger.debug("Copying {} modules. src={} dst={}".format(item_type, src, dest))
        shutil.copytree(src, dest)

        # add the item to the configurations.
        logger.debug(
            "Registering the {} into {}".format(item_type, DEFAULT_AEA_CONFIG_FILE)
        )
        existing_ids.add(PublicId(author_name, item_name, DEFAULT_VERSION))
        ctx.agent_loader.dump(
            ctx.agent_config, open(os.path.join(ctx.cwd, DEFAULT_AEA_CONFIG_FILE), "w")
        )

        # ensure the name in the yaml and the name of the folder are the same
        config_filepath = Path(
            ctx.cwd, item_type_plural, item_name, default_config_filename
        )
        config = loader.load(config_filepath.open())
        config.name = item_name
        config.author = author_name
        loader.dump(config, open(config_filepath, "w"))

    except FileExistsError:
        logger.error(
            "A {} with this name already exists. Please choose a different name and try again.".format(
                item_type
            )
        )
        sys.exit(1)
    except ValidationError:
        logger.error(
            "Error when validating the {} configuration file.".format(item_type)
        )
        shutil.rmtree(os.path.join(item_type_plural, item_name), ignore_errors=True)
        sys.exit(1)
    except Exception as e:
        logger.exception(e)
        shutil.rmtree(os.path.join(item_type_plural, item_name), ignore_errors=True)
        sys.exit(1)
