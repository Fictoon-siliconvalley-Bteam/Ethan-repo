#!/bin/sh
cd app/style_transfer_pytorch
su -m app -c "celery -A tasks worker --loglevel INFO"  