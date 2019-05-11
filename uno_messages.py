# -*- coding: utf-8 -*-

import json
import logging

logger = logging.getLogger(__name__)
messages = None


def initialize_messages_config():
    global messages
    """"Charge la configuration de messages"""
    config_path = 'resources/messages.json'

    with open(config_path, 'rt', encoding="utf-8") as f:
        messages = json.load(f)

    logger.info('Configuration de messages initialisée avec succès !')
