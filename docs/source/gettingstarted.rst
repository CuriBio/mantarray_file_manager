.. _gettingstarted:

Installing Mantarray File Manager
==================================

We recommend using Jupyter Notebooks to install the mantarray-file-manager. This
section will walk you through the process of using Jupyter notebooks and installing the
package.


First thing first, is to make sure you have python dowloaded to your PC. To do so,
proceed to the following website to download it: https://www.python.org/downloads/

As you are downloading this, make sure to select the options for installing pip
and on the next page the option for "Add Python to Environment Variables"

Here are images below to show what should be selected in full:

.. figure:: /images/python_install.PNG
.. figure:: /images/python_install_2.PNG


Once python has been installed we will now install Jupyter for Jupyter Notebooks.

To do so on Windows type "cmd" into the search on the taskbar to open up the command
terminal. From here you will want to follow these commands:

 * First you want to make sure your pip is up to date: python -m pip install --upgrade pip
 * Then you want to install Jupyter: python -m pip install jupyter

Once the installation completes to run the Jupyter Notebooks type: jupyter notebook

This should take you to a browser where you locally host your own Jupyter Notebook server


Now you’re in the Jupyter Notebook interface, and you can see all of the files in your current directory.
All Jupyter Notebooks are identifiable by the notebook icon next to their name.
If you already have a Jupyter Notebook in your current directory that you want to view,
find it in your files list and click it to open.

To create a new notebook, click New --> Notebook --> Python 3

Once inside the notebook you will see it contains a cell.

.. figure:: /images/empty_cell.jpg

Cells are how notebooks are structured and are the areas where you write your code.
To run a piece of code, click on the cell to select it, then press SHIFT+ENTER or press
the play button in the toolbar above.

Now that Jupyter Notebooks is installed and ready to use, we will now walk through getting the package installed and ready for use.
 * In the first cell type: !pip install curibio.sdk
 * Shift + Enter to run that cell and you should see a message after it is installed "Successfully installed curibio.sdk-0.1 h5py-2.10.0"

From here you are ready to proceed with using th package as described in the :ref:`Working with the package <usingthesdk>`.
