# Open LISA Server - Architecture

## Physical View

The following device and deploy diagrams shows the different hardware components and his services/interfaces involved
in end-to-end Open LISA experience.

![open_lisa_architecture](https://user-images.githubusercontent.com/45921171/195215569-f92946ba-066e-493d-a0c1-76c4ffdb0531.png)

[![Deploy Diagram](https://tinyurl.com/2lqddl5b)](https://tinyurl.com/2lqddl5b)<!--![Deploy Diagram](./deploy_diagram.puml)-->

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

In Open LISA there are two types of commands supported

* SCPI Command
* C Library Command

Each command is modeled by a corresponding class which implements `Command` interface.

The diagram below shows an example of execution for a SCPI command for turning on a channel in a oscilloscope

[![SCPI Command Example](https://tinyurl.com/2knrx67r)](https://tinyurl.com/2knrx67r)<!--![SCPI Command Example](./sequence_diagram_scpi_command.puml)-->

Finally, the diagram below shows an example for C Library Command. In this case we assume that we have a High Speed Camera with a DLL and specific functions for get a video record. It is important to understand that what it is executed in `C Library` depends on Open LISA User and what it is in `Camera DLL` depends on the instrument maker.

[![C Library Command Example](https://tinyurl.com/2mbatxgm)](https://tinyurl.com/2mbatxgm)<!--![C Library Command Example](./sequence_diagram_clib_command.puml)-->
