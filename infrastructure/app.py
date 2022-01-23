#!/usr/bin/env python3
from aws_cdk import core as cdk
from stacks.chaliceapp import (
    WhatsappBotStack, 
    # ChaliceSNS
)

app = cdk.App()
WhatsappBotStack(app, 'wp-bot-cdk')


app.synth()
