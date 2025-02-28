# Garmin Connect MCP Server

This project provides a server for interacting with the Garmin Connect API. It allows users to manage their Garmin data, including workouts, health metrics, and more.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages (install via `uv sync`)
- A Garmin Connect account
- Uses Python Garmin Connect Package to interact with Garmin Connect API: https://github.com/cyberjunky/python-garminconnect

### Environment Variables

Create a `.env` file in the root directory from the `.env_template` file with the following variables:

- `GARMIN_EMAIL`
- `GARMIN_PASSWORD`

## Generate token for Garmin Connect

```bash
python example.py
```

## Use MCP Inspector

```bash
mcp dev garmin_mcp_server.py
```

## Register MCP Server in Claude Desktop

```bash
mcp install garmin_mcp_server.py
```

### Running the Server


