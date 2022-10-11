# Open LISA Server - Architecture

## Logic view

The main classes involved for the server are shown in the following class diagram

[![Class Diagram OpenLISA](https://tinyurl.com/2pl3aads)](https://tinyurl.com/2pl3aads)

[![Class Diagram Protocol](https://tinyurl.com/2nbx5fss)](https://tinyurl.com/2nbx5fss)

[![Class Diagram Command](https://tinyurl.com/2n8rdg5z)](https://tinyurl.com/2n8rdg5z)

## Development view

The packages diagram below, shows how the modules are organized in the server side of Open LISA project

[![Packages Diagram](https://tinyurl.com/2pnxuaj3)](https://tinyurl.com/2pnxuaj3)


## Processes view

For the processes view, below are some sequence diagrams detailing interactions of interest involve in Open LISA Server

First, is important to understand the high level interactions between the client, server and their communication channel in the process of handling any generic command. The following diagram show the main interactions for handling a generic command with name `COMMAND_ID` which receives `command_params`

[![Generic Open LISA Command Execution](https://tinyurl.com/2jrjozob)](https://tinyurl.com/2jrjozob)<!--![Generic Open LISA Command Execution](./sequence_diagram_client_interaction_for_generic_command.puml)-->

In the following diagram we can see the actors involved in handling a request of command execution for an instrument (regardless if it is SCPI or CLib type)

[![Generic Command Execution Request](https://tinyurl.com/2gnnfclw)](https://tinyurl.com/2gnnfclw)<!--![Generic Command Execution Request](./sequence_diagram_generic_instrument_command.puml)-->
