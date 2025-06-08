# Model Context Protocol for ISO New England Energy Grid Information

This project implements a Model Context Protocal (MCP) Server for information on New Englands power grid.
Data is sourced from [ISO New England](https://iso-ne.com), which oversees the day-to-day operation of
the New England Power Grid.  This MCP server is built atop the ISO Express web services API from ISO New England, documented at [https://webservices.iso-ne.com/docs/v1.1/]


## What is an MCP Server and Why Do We Need One

An MCP server is a standardized interface to provide "tools" for artificial intelligence models, in particular, large language models (LLMs).  A canonical example is a question to an LLM like "what is the weather in San Fransciso right now?".  An LLM can't answer that on its own.  It needs a "tool" to be able to go and get the weather right now to answer that question

## What do you need to use this MCP Server
You need to create a [free ISO Express account](https://www.iso-ne.com/isoexpress/login) with ISO New England to get a username and password

## What questions can this MCP server answer

Example Question: What is the marginal fuel right now in new england?
Example Answer: The marginal fuel is Natural Gas and Wood 
Internal Implementation: accesses the /genfuelmix/current api endpoint
Note: The marginal fuel is the type of power that will be used if you wanted to use power on the grid right now, how would the grid provide that additional power

## What is the base api for iso-ne
The base api for the iso-new webservices api is [https://webservices.iso-ne.com/api/v1.1]