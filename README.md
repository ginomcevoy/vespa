# Vespa (Virtualized Experiments for Scientific Parallel Applications)

Vespa is designed to support the definition and production of controlled application executions running on virtual machines (VMs), as well as gathering performance metrics related to these executions. The main goal of Vespa is to manage the systematic experimentation of applications deployed on different virtual clusters, while supporting rich definitions for the cluster topology and mappings to underlying physical resources. The results will later translate into a knowledge repository with real (non-simulated) data for studying the effects of virtual cluster features on different scientific applications.

Vespa is not meant to be a tool for deploying applications in the Cloud or in virtualized environments. It is specifically aimed at improving the understanding of how virtualization affects application performance. While Vespa performs the deployment of the virtual cluster and the execution of the application, it does not currently configure the VMs (assumes the VM images are ready), nor does it takes care of the application deployment (assumes the application has an executable properly installed and ready to be called).

## Dependencies

Since Vespa is meant to be deployed on a physical cluster and support virtual clusters, there are different sets of dependencies:

### Common requirements
- Python 2.7.x
- Libvirt 1.x+ (libvirt-bin package)
- OpenSSH Server (openssh-server package) with password-less login between physical nodes and VMs 

### Requirements for head node
- Ansible 1.9+: Distributions may lag behind this requirement, use:
'''
sudo pip install ansible
'''
- Jinja 2 (included as dependency with Ansible)
- GNU parallel (parallel package)
- Torque server and Torque client (torque-server torque-client packages)
- NFS or equivalent for shared files in the physical cluster

### Requirements for computing nodes
- KVM
- Torque Node Manager (torque-mom package)
- Sysstat monitoring (sysstat package)

### Requirements for the VMs
- OpenMPI 1.8.x or newer: RPM or compiled from source,  see https://www.open-mpi.org/software/ompi/v1.8/

## Acknowledgments
This work is supported by the Brazilian National Research Council (CNPq), grant no. 150724/2015-2.