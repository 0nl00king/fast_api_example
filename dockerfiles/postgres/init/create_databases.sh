#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 <<-EOSQL
    CREATE DATABASE stcnet_admin;
    CREATE DATABASE stcnet_front;
    CREATE DATABASE stcnet_shared;
    CREATE DATABASE stcnet_flood;
EOSQL
