# Depl0y - Automated VM Deployment Panel for Proxmox VE
[https://agit8or.net/](Agit8or.net)

Live & Active

Depl0y
------

Automated VM Deployment Panel for Proxmox VE. Deploy VMs in 30 seconds with cloud images, comprehensive High Availability support, and multi-hypervisor management - all in a modern, intuitive interface.

Version 1.1.0 - Now Available

Overview
--------

Depl0y is a free, open-source automated VM deployment panel designed specifically for Proxmox VE. Built with modern technologies (Python 3.11+ and Vue.js 3.x), it revolutionizes VM management with ultra-fast cloud image deployments and enterprise-grade High Availability features.

Whether you're managing a single Proxmox node or a multi-node cluster, Depl0y provides MSPs and IT professionals with powerful tools for rapid VM provisioning, automated configuration with cloud-init, and wizard-guided HA setup - all through an intuitive web interface.

### Quick Facts

*   **Version:** 1.1.0
*   **Platform:** Proxmox VE
*   **Type:** Web-Based Panel
*   **Cost:** 100% Free
*   **License:** MIT License
*   **Status:** Live & Active

Key Features
------------

#### 30-Second Deployments

Deploy VMs in just 30 seconds using cloud images for Ubuntu, Debian, CentOS, Rocky Linux, Alma Linux, and Windows.

#### Cloud-Init Integration

Automatic VM configuration with cloud-init support for user setup, SSH keys, network configuration, and custom scripts.

#### High Availability

Wizard-guided HA setup with automatic VM failover, resource management, and cluster-wide monitoring.

#### Multi-Hypervisor Support

Manage multiple Proxmox VE nodes and clusters from a single interface with centralized control.

#### ISO Management

Built-in ISO library with pre-configured templates and custom ISO upload capabilities.

#### Resource Monitoring

Real-time monitoring of CPU, memory, disk, and network usage across all VMs and nodes.

#### 2FA Authentication

Enhanced security with two-factor authentication and role-based access control for multi-user environments.

#### Update Management

Automated update detection and management for both the panel and deployed VMs.

#### RESTful API

Complete API access for automation, integration with existing tools, and custom workflows.

#### Multi-User Support

Role-based access control with granular permissions for teams and organizations.

#### Encrypted Credentials

Secure storage of Proxmox credentials with encryption at rest for maximum security.

#### QEMU Guest Agent

Enhanced VM management with QEMU Guest Agent integration for better performance and control.


Why Choose Depl0y?
------------------

#### Lightning Fast

Deploy fully configured VMs in just 30 seconds using optimized cloud images.

#### Completely Free

Open source with MIT license - no subscriptions, no hidden costs, complete freedom.

#### Enterprise Ready

Production-grade HA support, 2FA, encrypted credentials, and role-based access control.

#### Intuitive Interface

Modern Vue.js interface with wizards and guided workflows for complex tasks.

#### Automation First

Full RESTful API for automation, scripting, and integration with your existing tools.

#### Team Friendly

Multi-user support with granular permissions perfect for IT teams and MSPs.

Technical Details
-----------------

### System Requirements

*   Ubuntu Server 22.04 LTS or 24.04 LTS
*   Python 3.11 or newer
*   Proxmox VE 7.x, 8.x, or 9.x
*   2GB RAM minimum (4GB recommended)
*   Modern web browser

### Technology Stack

*   Backend: Python 3.11+ with FastAPI
*   Frontend: Vue.js 3.x
*   Database: SQLite
*   Web Server: nginx (reverse proxy)
*   API: RESTful with Proxmox VE integration

### Supported Operating Systems

*   Ubuntu 20.04, 22.04, 24.04
*   Debian 11, 12
*   CentOS Stream 8, 9
*   Rocky Linux 8, 9
*   Alma Linux 8, 9
*   Windows Server (via cloud images)

### Availability

Depl0y is a free, open-source project designed for IT professionals and MSPs.

**Version:**  
1.1.0 (Latest)

**License:**  
MIT License

**Cost:**  
100% Free

**Support:**  
Community & Documentation

Get Started
-----------

### Ubuntu Server Installation

Install Depl0y on Ubuntu Server with this simple one-line command:

`curl -fsSL http://deploy.agit8or.net/install.sh | sudo bash`

The installation script will automatically install all dependencies, configure the web interface, and set up nginx reverse proxy. Installation takes approximately 2-3 minutes.

### Post-Installation

After installation completes:

*   Access the panel at `https://your-server-ip`
*   Default credentials will be displayed in the terminal
*   Add your Proxmox VE server(s) in Settings
*   Start deploying VMs in seconds!

### Quick Install

*   **Platform:** Ubuntu 22.04/24.04
*   **Time:** ~2-3 minutes
*   **Requirements:** Root access
*   **Method:** One-line install

Safe & secure installation

Production ready

Ready to Automate Your VM Deployments?
--------------------------------------

Contact us to learn more about Depl0y and how it can transform your Proxmox VE infrastructure.
