#!/usr/bin/env bash
# scripts/gen-env.sh

UID=$(id -u)
GID=$(id -g)
DID=$(getent group docker | cut -d: -f3)

sed \
  -e "s/@UID@/${UID}/g" \
  -e "s/@GID@/${GID}/g" \
  -e "s/@DID@/${DID}/g" \
  .env.template > .env

#docker compose up -d
