#!/bin/bash

docker compose up -d

docker compose wait webscraper > /dev/null

docker compose down