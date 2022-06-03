#!/bin/bash

WEBHOOK_URL=http://el-ed-app-event-listener-ed-app.apps.cluster-kv2bz.kv2bz.sandbox734.opentlc.com/

curl -i --header "Content-Type: application/json" -XPOST $WEBHOOK_URL -d '{"repository": {"html_url": "https://github.com/jwerak/ed-app","name": "ed-app"}, "ref": "0.0.4"}'


