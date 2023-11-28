# similariGAIT / gaitexplorationtool

## INSTALLATION

# Steps before running this program

* YOU ONLY HAVE TO DO THIS ONCE *
* Download docker for your OS from https://docs.docker.com/get-docker/ and install it
* Download the Git Repositoty for this tool from https://github.com/selimhoepler/bachelorabeit-one and extract the files in a place of choice


* now check if Docker is running by
  *  checking if the icon shows up
  *  or running docker desktop 
  *  or typing `docker`in your terminal and you are NOT getting an error
  
* if docker is running

* Inside your folder (the one where the downloaded repo is located at), open a new terminal window.
* Explanation for every OS: https://www.groovypost.com/howto/open-command-window-terminal-window-specific-folder-windows-mac-linux/

* in your terminal type `docker build -t similariGAIT .`
* wait until it is finished
* if an error occurs, try again or check if your terminal is INSIDE the folder where the Dockerfile is located

## Running the program

* After having done the steps above open your terminal anywhere and run `docker run -p 80:80 similariGAIT`
* Wait for the server to load up and navigate to 'http://127.0.0.1:80'



## Program explanation

# Data input

* put your .csv with the main data into the 'data-input' and your metadata .csv into the 'metadata-input' and press submit
* wait for the success message
* if everything works, the bottom sections should now be accessible

# Creating models

* select a setting for t-SNE or UMAP and create the model
* for more information about the parameters click the infobox
* this is the model whic will run on your data and provide the visualization

# Signal selection

* You can chose between provided signals to be included in the data the model will be run on
* On the left box, select to include the signal and on the right side the boxes are for the sagittal, frontal and transversal signal
* send signals and wait for the success message

# Model Execution

* Here you can run the model on the filtered data
* choose the affected legs, which will decide which patients are included in the clustering
* If there is an error
  * make sure you created a model
  * make sure you chose signals
  * maybe try different signals (Could be something wrong with NaN rows in the data)
  * maybe try a different 'affected leg' setting

* wait for the visualization

# Highlighting attributes

* you can choose between 'union-highlighting' and 'intersection-highlgting'
* The difference is explained in the infobox
* Select different attributes and see which points are highlighted

# Interacting with the visualization

* Hover over a datpoint to see general information about this patient
* Select the Lasso tool on the top right to select a set of datapoints, scroll down to see the attribute distribution of the selected datapoints in a bar chart
* when a set of points is highlighted, scroll down to see the attribute distribution of the highlighted datapoints in a bar chart
* when you click on a datapoint, scroll down to see all the attributes which correspond to this specific datapoint
* You can zoom in and out on the visualization
* you can download the current visualization and highlihting as PNG, SVG or CSV(only coordinates)
  








