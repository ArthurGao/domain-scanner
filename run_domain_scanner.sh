#!/bin/bash
export POSTGRES_USER=data_domain_scaner
export POSTGRES_PASSWORD=data_domain_scaner
export POSTGRES_HOST=localhost
export POSTGRES_DB=data_domain_scaner

cd /Users/arthurgao/Code/python/domain-scanner && PYTHONPATH=/Users/arthurgao/Code/python/domain-scanner /Users/arthurgao/.local/bin/uv run app/mcp/mcp_scan_server.py