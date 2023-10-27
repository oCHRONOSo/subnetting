# Subnetting Calculator

Subnetting Calculator is a Python application that helps you calculate subnets for a given IP address and subnet mask. It provides both a graphical user interface (GUI) and a command-line interface (CLI) for your convenience.

## Table of Contents
- [Subnetting Calculator](#subnetting-calculator)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Windows](#windows)
  - [Linux](#linux)
- [Usage](#usage)
  - [GUI Usage](#gui-usage)
  - [CLI Usage](#cli-usage)
  - [Features](#features)

## Prerequisites

Before using Subnetting Calculator, make sure you have Python installed. You can check if Python is installed by running the following command:

```shell
python --version
```
If Python is not installed, follow the installation instructions below for your specific operating system.

# Installation
## Windows
Download the latest Python installer for Windows from the official Python website.
Run the installer and follow the on-screen instructions to install Python.
## Linux
You can install Python on most Linux distributions using the package manager. For example, on Debian/Ubuntu-based systems, you can use:

```shell
sudo apt-get install python
```
On Red Hat/Fedora-based systems, you can use:
```shell
sudo dnf install python
```
# Usage
Subnetting Calculator can be used either through the GUI or the CLI. The application takes an IP address, subnet mask, and allows you to calculate subnets based on the number of subnets or the number of hosts.

## GUI Usage
To run the GUI, execute the following command:

```shell
python ip_GUI.py
```
## CLI Usage
To run the CLI, execute the following command:

```shell
python ip.py
```
## Features
- Calculate subnets based on the number of subnets or the number of hosts.
- Validate input data, including IP addresses and subnet masks.
- Display subnet network IP, first/last host IP, and broadcast IP for each subnet.