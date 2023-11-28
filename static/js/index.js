



// declaring Constant variables

const dataSubmitBtn = document.getElementById('data-submit-button');
const inputFilesData = document.getElementById('input-data');
const inputFilesMetadata = document.getElementById('input-metadata');

const perplexitySlider = document.getElementById('tsne-perplexity-slider');
const iterationsSlider = document.getElementById('tsne-iterations-slider');

const minDistSlider = document.getElementById('umap-minDist-slider');
const nNeighborsSlider = document.getElementById('umap-n-neighbors-slider');

const presetDropdown = document.getElementById("preset-dropdown");
const sendButton = document.getElementById("send-button");

const attributeContainer = document.getElementById("attribute-checkbox-container")

const modelsButton = document.getElementById("models-button-tsne");

const modelButtons = document.querySelectorAll('.models-button')

const executeButton = document.getElementById("execute-button");

const blurryContainers = document.querySelectorAll(".blurryCont");


// var for the charts 
var chart;

var infoChart;

// helper for the chart updates
var discreteList = [];

var firstClick = true;

var tooltipData = [];

var attributeData = [];

let sumAttributes = true;
let leg = 'both'

const sumHighlightBtn = document.getElementById("sumHighlightBtn");
const intHighlightBtn = document.getElementById("intersectionHighlightBtn");

const legBtnBoth = document.getElementById('leg-btn-both');
const legBtnIndividual = document.getElementById('leg-btn-individual');
const legBtnAll = document.getElementById('leg-btn-all');








/* 
Data input section
 */


dataSubmitBtn.addEventListener('click', async () => {
    // Check Datatype extension
    const allowedExtensions = ['csv'];
    const dataFile = inputFilesData.files[0];
    const metadataFile = inputFilesMetadata.files[0];


    // minor file validation
    if (!allowedExtensions.includes(dataFile.name.split('.').pop())) {
        console.error('Fehler: Ungültige Dateierweiterung für Data-Datei');
        return;
    }

    if (!allowedExtensions.includes(metadataFile.name.split('.').pop())) {
        console.error('Fehler: Ungültige Dateierweiterung für Metadata-Datei');
        return;
    }

    // Change style of input btn 
    dataSubmitBtn.textContent = 'Loading...';
    dataSubmitBtn.disabled = true;
    dataSubmitBtn.classList.remove('hover:bg-indigo-600');

    // Make formData Object to collect Files
    const formData = new FormData();
    formData.append('data_file', dataFile, 'data.csv');
    formData.append('metadata_file', metadataFile, 'metadata.csv');


    // try sending both files to the backend with the route '/ingest'
    //
    try {
        const response = await fetch('/ingest', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {

            const data = await response.json();
            console.log(data);

            //filtering the data for the usable info for signal and attribute checkboxes
            const checkBoxData = data.response.checkboxes;
            console.log(checkBoxData);

            const attributes = data.response.attributes
            console.log(attributes)

            // Create Checkboxes
            createSignalCheckboxes(checkBoxData);
            createAttributeCheckboxes(attributes)


            // enable preset selection 
            blurryContainers.forEach((element) => {
                element.classList.remove('opacity-30');
                element.classList.remove('pointer-events-none')
            });


            presetDropdown.disabled = false;
            sendButton.disabled = false;
            sendButton.classList.add('hover:bg-blue-600');

            showToast('Data succesfully uploaded', 'success')
        } else {
            console.error('Fehler beim Senden der Dateien:', response);
            showToast('Error while loading data', 'danger')
        }
    } catch (error) {
        console.error('Fehler beim Senden der Dateien:', error);
        showToast('Error while loading data', 'danger')
    } finally {
        // Change button styling back
        dataSubmitBtn.textContent = 'Submit';
        dataSubmitBtn.disabled = false;
        dataSubmitBtn.classList.add('hover:bg-blue-600');


    }
});






///
/// checkboxes Section
///


// This function creates the signal checkboxes. Each signal gets One Checkbox to be enabled and then 3 checkboxes for
// sag, front, trans as in sagittal, frontal and transversal planes of the human body
function createSignalCheckboxes(jsonData) {
    const container = document.getElementById('signal-checkbox-container');

    // Parse the JSON data
    const data = jsonData;

    // Create checkboxes for angle/moment values
    for (const keys in data) {


        for (const key in data[keys]) {


            const checkboxData = data[keys][key];

            const checkboxContainer = document.createElement('div');
            checkboxContainer.classList.add('flex');
            checkboxContainer.classList.add('justify-between');
            checkboxContainer.classList.add('checkbox-subcontainer');

            // Create enabled checkbox
            const enabledCheckbox = document.createElement('input');
            enabledCheckbox.type = 'checkbox';
            enabledCheckbox.name = key;
            enabledCheckbox.checked = checkboxData.enabled;

            checkboxContainer.appendChild(enabledCheckbox);

            // Create label for checkbox
            const boxesLabel = document.createElement('label');
            boxesLabel.classList.add('dark:text-white')
            boxesLabel.textContent = key;
            checkboxContainer.appendChild(boxesLabel);

            // create sag trans front checkboxes
            const signalCheckboxes = document.createElement('div');
            signalCheckboxes.classList.add('signalboxes-container');
            for (const i in checkboxData) {
                if (i !== 'enabled') {
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.name = String(key + i);
                    checkbox.checked = checkboxData[i];
                    signalCheckboxes.appendChild(checkbox);
                }
                checkboxContainer.appendChild(signalCheckboxes);
            }


            // Add the checkbox container to the main container
            container.appendChild(checkboxContainer);
        }

    }




}


// this function cretes checkboxes out of all the attributes received from the backend
function createAttributeCheckboxes(jsonData) {
    const container = document.getElementById('attribute-checkbox-container');

    // Parse the JSON data
    const int_data = jsonData.int_attributes;
    const string_data = jsonData.string_attributes;



    for (const category in string_data) {


        for (const key in string_data[category]) {



            const checkboxContainer = document.createElement('div');
            checkboxContainer.classList.add('flex');
            checkboxContainer.classList.add('justify-between');
            checkboxContainer.classList.add('string-attributes-checkbox-subcontainer');

            // Create label for checkbox
            const boxesLabel = document.createElement('label');
            boxesLabel.textContent = string_data[category][key];
            boxesLabel.classList.add('dark:text-white')
            checkboxContainer.appendChild(boxesLabel);

            // Create checkbox
            const attributeCheckbox = document.createElement('input');
            attributeCheckbox.type = 'checkbox';
            attributeCheckbox.name = string_data[category][key];

            checkboxContainer.appendChild(attributeCheckbox);

            // Add the checkbox container to the main container
            container.appendChild(checkboxContainer);

        }


    }


    // Create checkboxes 
    for (const element in int_data) {

        // Filtering specific unnecessary attributes. (TODO: ask a professional, which attributes are important, which are not)
        if (int_data[element] !== 'Vorname' && int_data[element] !== 'DBId' && int_data[element] !== 'Num_Matfiles') {
            const checkboxContainer = document.createElement('div');
            checkboxContainer.classList.add('flex');
            checkboxContainer.classList.add('justify-between');
            checkboxContainer.classList.add('attributes-checkbox-subcontainer');



            // Create label for checkbox
            const boxesLabel = document.createElement('label');
            boxesLabel.textContent = int_data[element];
            boxesLabel.classList.add('dark:text-white')
            checkboxContainer.appendChild(boxesLabel);

            // Create checkbox
            const attributeCheckbox = document.createElement('input');
            attributeCheckbox.type = 'checkbox';
            attributeCheckbox.name = int_data[element];

            checkboxContainer.appendChild(attributeCheckbox);


            // Add the checkbox container to the main container
            container.appendChild(checkboxContainer);
        }


    }
}




// 
// Signal selection section
//




// Adding an event listener to send the selected presets or cehcked boxes to the backend. 
document.addEventListener("DOMContentLoaded", function () {


    sendButton.addEventListener("click", async () => {



        const preset = getSignalJSON();


        if (preset.signals.length !== 0) {

            sendButton.textContent = 'Loading...';
            sendButton.disabled = true;
            sendButton.classList.remove('hover:bg-indigo-600');
            // The array is not empty

            // try sending preset to the backend
            try {
                const response = await fetch("/signals", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(preset),
                });

                if (response.ok) {

                    console.log("Option successfully sent to backend.");
                    console.log(await response.json());
                    showToast('Successfully read signals', 'success');
                } else {

                    console.error("Error while sending option to the backend:", response.statusText);
                    showToast('Error while reading signals', 'danger');
                }
            } catch (error) {

                console.error("Error while sending option to the backend:", error);
                showToast('Error while reading signals', 'danger');
            } finally {

                // reset send Button
                sendButton.textContent = 'Send';
                sendButton.disabled = false;
                sendButton.classList.add('hover:bg-indigo-600');
            }
        } else {
            showToast('please select at least one signal and one type', 'warning');
        }
    });
});




// function to get the signal JSON
const getSignalJSON = () => {

    const container = document.getElementById('signal-checkbox-container');

    const signals = [];
    const columns = [];

    const subContainer = container.querySelectorAll('.checkbox-subcontainer');
    //iterate through the subcontainers
    subContainer.forEach((subContainer) => {
        //get the checkbox
        const checkbox = subContainer.querySelector('input[type="checkbox"]');
        //check if the checkbox is checked
        if (checkbox.checked) {
            signals.push(checkbox.name);

            const checkedColumns = [];

            const signalBoxesContainer = subContainer.querySelector('.signalboxes-container');
            const signalBoxes = signalBoxesContainer.querySelectorAll('input[type="checkbox"]');


            // This part exists because the presets.json uses the numbers 1,3,5 to identify 
            //if either sag, trans or front was selcted
            signalBoxes.forEach((signalBox, index) => {
                if (signalBox.checked) {
                    checkedColumns.push(index + index + 1);
                }
            });

            columns.push(checkedColumns);
        }
    });

    // structures object into signals and columns 
    const signalData = {
        signals: signals,
        columns: columns
    }

    console.log(signalData);


    return signalData;



}


//turning presets into checkboxes
function convertPresetToCheckboxes2(preset) {
    const container = document.getElementById('signal-checkbox-container');
    const subContainers = container.querySelectorAll('.checkbox-subcontainer');

    // Iterate through the subcontainers
    subContainers.forEach((subContainer, index) => {
        const checkbox = subContainer.querySelector('input[type="checkbox"]');

        //reset all checkboxes
        const signalBoxesContainer = subContainer.querySelector('.signalboxes-container');
        const signalBoxes = signalBoxesContainer.querySelectorAll('input[type="checkbox"]');

        // Reset all sub-checkboxes
        signalBoxes.forEach(box => {
            box.checked = false;
        });


        const checkboxName = checkbox.name;

        // Find the index of this checkbox name in the preset signals
        const matchingIndex = preset.signals.indexOf(checkboxName);

        // If found, set the main checkbox and sub-checkboxes accordingly
        if (matchingIndex !== -1) {
            checkbox.checked = true;

            const columnIndices = preset.columns[matchingIndex];
            const signalBoxesContainer = subContainer.querySelector('.signalboxes-container');
            const signalBoxes = signalBoxesContainer.querySelectorAll('input[type="checkbox"]');


            // Check the sub-checkboxes according to preset
            columnIndices.forEach(idx => {
                const boxIndex = (idx - 1) / 2; // Convert the 3-based index to 0-based (Again, because of 1,3,5)
                if (signalBoxes[boxIndex]) {
                    signalBoxes[boxIndex].checked = true;
                }
            });
        } else {
            // Uncheck the main checkbox if it is not in the preset
            checkbox.checked = false;
        }
    });
}




// Gets the names of all checked attributes in a list. Returns the list
function getCheckedAttributes() {
    const container = document.getElementById('attribute-checkbox-container')


    const checkedCheckboxes = container.querySelectorAll('input:checked')

    var checkedList = []

    checkedCheckboxes.forEach(element => {
        checkedList.push(element.name)
    });


    return checkedList
}

// helper function for getSelectedDatapoints
// checks if the specific datapoint already has a checked attribute, if no it gets added with its value,
// if yes it gets added with different value
// values are needed for colorcodig in the visualization
function updateDbidList(dbidlist, dbid, incrementValue) {
    const found = dbidlist.find(item => Object.keys(item)[0] === dbid.toString());

    if (found) {
        found[dbid] += incrementValue;
    } else {
        dbidlist.push({ [dbid]: incrementValue });
    }
}




//This function gets a list for each index that has the attribute which is checked in the attributes section
function getSelectedDatapoints() {
    return new Promise((resolve, reject) => {

        // get a list of all the checked attributes
        const checkedAttributes = getCheckedAttributes();

        //resolve as an empty array if no attributes are seleected
        if (checkedAttributes.length === 0) {
            return resolve([]);
        }

        fetch('/static/json/attributes.json')
            .then(response => response.json())
            .then(data => {
                const dbid = data.columns.indexOf("DBId");
                var indexlist = [];
                var dbidlist = [];

                // get the indexes of each checked attribute, to filter the data
                data.columns.forEach(element => {
                    if (checkedAttributes.includes(element)) {
                        indexlist.push(data.columns.indexOf(element));
                    }
                });

                console.log(indexlist);
                // Depending on sumAttributes, return a list of indices either of the points that match ONE of the checked attributes
                // or the points that match ALL of the checked attributes
                if (sumAttributes) { // EITHER of the attributes
                    data.data.forEach(row => {
                        indexlist.forEach(index => {
                            if (row[index] === 1) {
                                const incrementValue = checkedAttributes.indexOf(data.columns[index]) + 1;
                                updateDbidList(dbidlist, row[dbid], incrementValue);
                            }
                        });

                        // Check for attributes with string values
                        row.forEach(value => {
                            checkedAttributes.forEach(attribute => {
                                if (value === attribute) {
                                    const incrementValue = checkedAttributes.indexOf(attribute) + 1;
                                    updateDbidList(dbidlist, row[dbid], incrementValue);
                                }
                            });
                        });
                    });



                } else { // ALL of the attributes
                    data.data.forEach(row => {
                        let matchCount = 0;

                        // Check for integer attributes (1s)
                        indexlist.forEach(index => {
                            if (row[index] === 1) {
                                matchCount++;
                            }
                        });

                        // Check for attributes with string values
                        row.forEach(value => {
                            checkedAttributes.forEach(attribute => {
                                if (value === attribute) {
                                    matchCount++;
                                }
                            });
                        });

                        // If the number of matches equals the number of checked attributes, add the dbid
                        if (matchCount === checkedAttributes.length && !dbidlist.includes(row[dbid])) {
                            dbidlist.push({ [row[dbid]]: 1 });
                        }
                    });
                }

                resolve(dbidlist); // Resolve the promise with dbidlist
            })
            .catch(error => {
                console.error('Error:', error);
                reject(error); // Reject the promise with error
            });
    });
}



/* 

When an attribute checkbox is selected, the data on chart should be updated instantly

for that i get a list of indexes from getSelectedDatapoints, add an eventlistener to the checkboxes and update the chart 
where all z-values correspond to the ones in indexlist.

*/



attributeContainer.addEventListener('change', async (e) => {
    if (e.target.type === 'checkbox') {
        try {
            const indexList = await getSelectedDatapoints();




            // map datapoints from the ApexCharts instance
            chart.w.config.series[0].data.map((point, index) => {
                let value;
                const matchedObj = indexList.find(obj => obj.hasOwnProperty(point.z));


                if (matchedObj) {
                    value = matchedObj[point.z];
                    pushThisIndexAsDiscrete(index, value);  
                }

            });


            //ApexCharts updateOptions method
            chart.updateOptions({
                markers: {
                    size: 4,
                    discrete:
                        discreteList

                },
                chart: {
                    animations: {
                        enabled: false,
                    },
                },
            }, false, false, false);

            // reset List of selected indexes
            discreteList = [];




            // trigger the dataCloud infoBox change
            dataCloudSelected('attributeSelection', 0, 0);


        } catch (error) {
            console.error('Error in event listener:', error);
        }
    }
});



// sets color for specific Datapoint with value coming from the attributes 
function pushThisIndexAsDiscrete(index, value) {
    let color = '#C73E1D'

    switch (value) {
        case 1: {
            color = "#D95F02";

            break;
        }; // Color for both attribute match
        case 2: {
            color = "#7570B3";

            break;
        }; // Color for 1 attribute matches
        case 3: {
            color = "#1B9E77";

            break;
        }; // Color for 2 attributes match
        default: {
            color = '#f0f0f0';

            break;
        };// Default color or no color
    }


    const discrete = {
        seriesIndex: 0,
        dataPointIndex: index,
        fillColor: color,
        strokeColor: "#FFF",
        size: 6
    }

    // push to global list, which will be used to update the visualization
    discreteList.push(discrete);
}








/* 
PRESETS FROM signals.json
-all_uc1
-thorax(andreas)
-knee_angles
-knee_angles&moments */


// eventlistener for the preset dropdown, when a preset is selected, the fuction convertPresetToCheckboxes  will becalled
// to check the boxes accordingly
presetDropdown.addEventListener("change", async () => {

    const preset = presetDropdown.value
    console.log(preset)

    if (preset != 'none') {
        fetch('/static/config/signals.json')
            .then(response => response.json())
            .then(data => {
                // Use the parsed JSON data here
                console.log(data)
                const myPreset = data[preset]
                console.log(myPreset);

                convertPresetToCheckboxes2(myPreset);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        //uncheck all boxes
        const container = document.getElementById('signal-checkbox-container');
        const subContainer = container.querySelectorAll('.checkbox-subcontainer');
        //iterate through the subcontainers
        subContainer.forEach((subContainer) => {
            //get the checkbox
            const checkbox = subContainer.querySelector('input[type="checkbox"]');
            checkbox.checked = false

            const signalBoxesContainer = subContainer.querySelector('.signalboxes-container');
            const signalBoxes = signalBoxesContainer.querySelectorAll('input[type="checkbox"]');

            // Reset all sub-checkboxes
            signalBoxes.forEach(box => box.checked = false);
        });
    }
});





//
// InfoBox Section
//



// gets called when a datapoint in the visualization is selected
// gets the 'ID' as z from the datapoint, 
// gets all attribute which correspond to this datapoint
// calls displayInformation to displays information ;)
async function dataPointSelected(index) {
    console.log('datapoint selected', index);
    console.log(chart.w.config.series[0].data[index]);

    const dataPointDBID = chart.w.config.series[0].data[index].z
    const age = chart.w.config.series[0].data[index].age

    try {
        const attributeNameArray = await getAttributes(dataPointDBID);
        var intAttributeNameList = attributeNameArray[0];
        var strAttributeNameList = attributeNameArray[1];
        strAttributeNameList.push(age)


        displayInformation(intAttributeNameList, strAttributeNameList);

        // when loading the app new and clicking a DP for the first time, user will be directed to the inofrmation section
        if (firstClick) {
            const element = document.getElementById("yellowCont");
            element.scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
            firstClick = false;
        }
    } catch (error) {
        console.error("Error while fetching attributes:", error);
    }
}


// get all the matching attributes for a specific DP with its 'DBID' from attributes.json
function getAttributes(dbid) {
    return new Promise((resolve, reject) => {
        var intAttributeNameList = [];
        var strAttributeNameList = [];

        fetch('/static/json/attributes.json')
            .then(response => response.json())
            .then(data => {
                const dbidIndex = data.columns.indexOf("DBId");

                // iterate through rows, if correct row: iterate through columns and push all columnnames which are set to 1 and all str cols
                data.data.forEach(row => {
                    if (row[dbidIndex] === dbid) {
                        row.forEach((col, colindex) => {
                            if (col === 1) {
                                intAttributeNameList.push(data.columns[colindex]);
                            } else if (typeof col === 'string') {
                                strAttributeNameList.push(col);
                            }
                        });
                    }
                });

                // retuns obj structured into int and str attributes
                resolve([intAttributeNameList, strAttributeNameList]);
            })
            .catch(error => {
                console.error("Error fetching attributes:", error);
                reject(error);
            });
    });
}



// display a chart of info of the selected cloud (either by attribute selection or brush selectioon)
// get all 1s and all strAttributes in attribute.json of the datapoints in cloud
// add number of attributes
// chart the distribution of attributes as a bar chart through displayCloudInformation
async function dataCloudSelected(method, xaxis, yaxis) {


    try {
        let selectedDatapoints
        if (method == 'attributeSelection') {
            selectedDatapoints = await getSelectedDatapoints();
        } else if (method == 'brushSelection') {
            selectedDatapoints = await getBrushDatapoints(xaxis, yaxis);
        }
        const response = await fetch('/static/json/attributes.json');
        const data = await response.json();

        const dbidIndex = data.columns.indexOf("DBId");

        var attributeStatisticList = [];

        // iterate through attribute rows to get the attribute
        data.data.forEach(row => {
            const matchedObj = selectedDatapoints.find(obj => obj.hasOwnProperty(row[dbidIndex]));
            if (matchedObj) {
                row.forEach((attribute, index) => {
                    if (attribute === 1) {
                        attributeStatisticList.push(data.columns[index])
                    }
                    if (typeof attribute === 'string') {
                        attributeStatisticList.push(attribute)
                    }
                });
            }
        });

        displayCloudInformation(attributeStatisticList);

    } catch (error) {
        console.error('Error:', error);
    }
}



// displays information in info-container about a single Datapoint
function displayInformation(intAttributeNameList, strAttributeNameList) {


    const generalInfoContainer = document.getElementById('general-info-container');
    const attributeInfoContainer = document.getElementById('attribute-info-container');

    generalInfoContainer.innerHTML = '';
    attributeInfoContainer.innerHTML = '';

    strAttributeNameList.forEach(attribute => {
        console.log(attribute);

        const generalInfoBox = document.createElement('div');
        generalInfoBox.classList.add('general-info-box');

        const newParagraph = document.createElement("p");
        newParagraph.textContent = attribute;

        generalInfoBox.appendChild(newParagraph);

        generalInfoContainer.appendChild(generalInfoBox);
        console.log(generalInfoContainer);
    })

    intAttributeNameList.forEach(attribute => {
        const attributeInfoBox = document.createElement('div');
        attributeInfoBox.classList.add('attribute-info-box');

        const newParagraph = document.createElement("p");
        newParagraph.textContent = attribute;

        attributeInfoBox.appendChild(newParagraph);

        attributeInfoContainer.appendChild(attributeInfoBox);
    })



}


// displays attribute distribution of selected cloud
function displayCloudInformation(attributeList) {
    // Preprocess data to get frequency of each unique value
    const frequency = attributeList.reduce((acc, val) => {
        acc[val] = (acc[val] || 0) + 1;
        return acc;
    }, {});

    // Create an array of objects from frequency
    const dataArray = Object.entries(frequency).map(([category, value]) => ({ category, value }));

    // Sort dataArray by value in descending order
    dataArray.sort((a, b) => b.value - a.value);

    // Extract sorted categories and data
    const categories = dataArray.map(obj => obj.category);
    const data = dataArray.map(obj => obj.value);



    // Check if infoChart exists
    if (infoChart) {
        // Update the existing chart with new data
        infoChart.updateOptions({
            series: [{
                name: '',
                data: data
            }],
            xaxis: {
                categories: categories
            }
        });


    } else {
        // Create chart
        var options = {
            chart: {
                height: '500px',
                type: 'bar'
            },
            series: [{
                name: '',
                data: data
            }],
            xaxis: {
                categories: categories
            }
        };

        infoChart = new ApexCharts(document.querySelector("#cloud-plot-container"), options);
        infoChart.render();
    }
}


// get ids from brsuhed selection, gets called when brush selection
function getBrushDatapoints(xaxis, yaxis) {
    return new Promise((resolve, reject) => {
        const points = chart.w.config.series[0].data
        let dbidlist = []

        points.forEach(point => {
            if (point.x > xaxis['min'] && point.x < xaxis['max'] && point.y > yaxis['min'] && point.y < yaxis['max']) {
                console.log(point.z)
                dbidlist.push({ [point.z]: 1 });
            }
        });

        console.log(dbidlist)
        resolve(dbidlist)
    });
}






//
// Model creating section
//
modelButtons.forEach(btn => {

    // if ccreate model btn is clicked, collect user specified settings and send it to backend
    btn.addEventListener("click", async () => {

        // get t-SNE or UMAP settings from user
        const perplexity = parseInt(perplexitySlider.value, 10);
        const iterations = parseInt(iterationsSlider.value, 10);

        // not customizable as of now
        const dMetricValue = "euclidean"

        const minDistValue = parseFloat(minDistSlider.value);
        const nNeighborsValue = parseInt(nNeighborsSlider.value, 10);

        console.log(btn.value)


        const modelType = btn.value;




        try {
            const response = await fetch("/models", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    tsne_settings: {
                        tsne_perplexity: perplexity,
                        tsne_iterations: iterations,
                        d_metric: dMetricValue
                    },
                    
                    umap_settings: {
                        min_dist: minDistValue,
                        n_neighbors: nNeighborsValue
                    },
                    selected_model_type: modelType
                })
            });


            if (response.ok) {
                console.log("Models successfully sent to backend.");
                console.log(await response.json());
                showToast('Models successfully loaded', 'success')

            } else {
                console.error("Fehler beim Senden der Modelle ans Backend:", response.statusText);
                showToast('Error while loading models', 'danger')
            }
        } catch (error) {
            console.error("Fehler1 beim Senden der Modelle ans Backend:", error);
            showToast('Error while loading models', 'danger')
        }
    });

});





//
// Model execution section
//

// get all tooltipdata from all datapoints
async function getTooltipData() {
    const data = chart.w.config.series[0].data;

    var tooltipDataArray = {};

    for (const index of data) {
        const dbid = index.z;
        const dataAttributes = await getAttributes(dbid);

        // hardcoded for now, has to be made differently when submitted data is different,
        // maybe provided files should have one specific affected site col 
        let affectedSide = '';
        if (dataAttributes[0].includes('UC1_betroffen_LI') && dataAttributes[0].includes('UC1_betroffen_RE')) {
            affectedSide = 'Both';
        } else if (dataAttributes[0].includes('UC1_betroffen_LI')) {
            affectedSide = 'Left';
        } else if (dataAttributes[0].includes('UC1_betroffen_RE')) {
            affectedSide = 'Right';
        }



        const stringAttributes = dataAttributes[1];

        // Structure the data for easy lookup by dbid
        tooltipDataArray[dbid] = { attributes: stringAttributes, affectedSide: affectedSide };
    }

    console.log(tooltipDataArray);

    return tooltipDataArray;  // Return the processed data
}



//
// Chart section
//



executeButton.addEventListener("click", async () => {
    try {
        console.log(typeof (leg));
        const intervalValue = 5;
        executeButton.textContent = 'Loading...';
        executeButton.disabled = true;
        executeButton.classList.remove('hover:bg-red-600');
        const response = await fetch("/execute", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            // or wherever you're getting this value from

            body: JSON.stringify({
                legs: leg, // Assuming leg is a string like "both"
                interval: intervalValue
            })


        });

        if (response.ok) {

            console.log("Models successfully executed.");

            const responseData = await response.json(); // JSON-Daten nur einmal lesen

            console.log(responseData);

            const series = responseData.scatterplot_data.map(item => ({
                x: item.x,
                y: item.y,
                z: item.z,
                age: item.age,

            }));


            if (chart) {
                // Update the existing chart with new data
                chart.updateOptions({
                    chart: {
                        animations: {
                            enabled: true,
                        },
                    },
                    series: [{
                        name: "Sample B",
                        data: series
                    }]
                });

                getTooltipData().then(data => {
                    tooltipData = data;
                });


            } else {

                var options = {
                    series: [{
                        name: "",
                        data: series
                    }],
                    chart: {
                        height: '100%',
                        type: 'scatter',
                        animations: {
                            enabled: true,
                        },
                        zoom: {
                            enabled: true,
                            type: 'xy'
                        },
                        events: {
                            markerClick: function (event, chartContext, { seriesIndex, dataPointIndex, config }) {
                                dataPointSelected(dataPointIndex);
                            },
                            selection: function (chartContext, { xaxis, yaxis }) {
                                console.log(xaxis, yaxis)
                                dataCloudSelected('brushSelection', xaxis, yaxis);
                            }
                        },
                        selection: {
                            enabled: true,
                            type: 'xy',
                            fill: {
                                color: '#24292e',
                                opacity: 0.1
                            },
                            stroke: {
                                width: 1,
                                dashArray: 3,
                                color: '#24292e',
                                opacity: 0.4
                            },
                            xaxis: {
                                min: undefined,
                                max: undefined
                            },
                            yaxis: {
                                min: undefined,
                                max: undefined
                            }
                        },

                    },
                    xaxis: {
                        show: false,
                        tickAmount: 10,
                        labels: {
                            show: false,
                        },

                    },
                    yaxis: {
                        show: false,
                        tickAmount: 7
                    },
                    markers: {
                        size: 4,
                        colors: ['#A6CEE3'],
                    }, tooltip: {
                        custom: function ({ series, seriesIndex, dataPointIndex, w }) {
                            var data = w.globals.initialSeries[seriesIndex].data[dataPointIndex];
                            //get 'dbID'
                            const dataPointDBID = chart.w.config.series[0].data[dataPointIndex].z

                            // get str attributes from attributes.json
                            var attributes
                            Object.keys(tooltipData).forEach(key => {

                                if (key == dataPointDBID) {

                                    attributes = tooltipData[key].attributes;
                                    affectedSide = tooltipData[key].affectedSide;
                                }

                            });





                            return '<ul>' +
                                '<li><b>ID</b>: \'' + data.z + '\'</li>' +
                                '<li><b>Age</b>: \'' + data.age + '\'</li>' +
                                '<li><b>Sex</b>: \'' + attributes[0] + '\'</li>' +
                                '<li><b>Rough category</b>: \'' + attributes[1] + '\'</li>' +
                                '<li><b>Affected Side</b>: \'' + affectedSide + '\'</li>' +
                                '</ul>';

                        }
                    }
                };

                chart = new ApexCharts(document.getElementById("plot-container"), options);
                chart.render();

                getTooltipData().then(data => {
                    tooltipData = data;
                });





            }
        } else {
            console.error("Something went wrong while executing:", response.statusText);
            if (response.status === 404){
                showToast('Something went wrong. It seems like you did not load a model or signals before!', 'danger')
            } if (response.status === 500){
            showToast('Something went wrong while executing. Maybe try a different set of signals!', 'danger')
            }
        }
    } catch (error) {
        console.error("Something went wrong while executing:", error);
        //showToast('Something went wrong while executing', 'danger')
    }
    finally {
        executeButton.textContent = 'Execute';
        executeButton.disabled = false;
        executeButton.classList.add('hover:bg-red-600');
    }
});







//
//// minor functions
//





//get the value of sliders
window.onload = function () {

    const tsnePerplexityOutput = document.getElementById("tsne-perplexity-value");
    const tsneIterationsOutput = document.getElementById('tsne-iterations-value');
    const umapMinDistOutput = document.getElementById('umap-minDist-value');
    const umapNNeighborsOutput = document.getElementById('umap-n-neighbors-value');

    tsnePerplexityOutput.value = perplexitySlider.value; // set the initial value on page load
    tsneIterationsOutput.value = iterationsSlider.value;
    umapMinDistOutput.value = minDistSlider.value;
    umapNNeighborsOutput.value = nNeighborsSlider.value;

    perplexitySlider.oninput = function () {
        tsnePerplexityOutput.value = this.value; // update the value when the slider changes
    }

    iterationsSlider.oninput = function () {
        tsneIterationsOutput.value = this.value; // update the value when the slider changes
        console.log(chart.w.config)
    }

    minDistSlider.oninput = function () {
        umapMinDistOutput.value = this.value; // update the value when the slider changes
    }

    nNeighborsSlider.oninput = function () {
        umapNNeighborsOutput.value = this.value; // update the value when the slider changes
    }

}


//toast-notifications


function showToast(message, type = 'success') {
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `flex items-center w-full max-w-xs p-4 mb-4 text-gray-500 bg-indigo-100 rounded-lg shadow dark:text-gray-400 dark:bg-gray-800 fixed top-5 right-5`;
    toast.setAttribute('role', 'alert');

    // Check icon container
    const iconContainer = document.createElement('div');
    iconContainer.className = `inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-${type}-500 bg-${type}-100 rounded-lg dark:bg-${type}-800 dark:text-${type}-200`;
    let iconSVG = ""
    // Check icon SVG
    if (type == 'success') {
        iconSVG = `<div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-green-500 bg-green-100 rounded-lg dark:bg-green-800 dark:text-green-200">
        <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/>
        </svg>
        <span class="sr-only">Check icon</span>
        </div>`;
    } else if (type == "danger") {
        iconSVG = `<div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-red-500 bg-red-100 rounded-lg dark:bg-red-800 dark:text-red-200">
        <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"/>
        </svg>
        <span class="sr-only">Error icon</span>
        </div>`
    } else if (type == 'warning') {
        iconSVG = `<div class="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-orange-500 bg-orange-100 rounded-lg dark:bg-orange-700 dark:text-orange-200">
        <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM10 15a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-4a1 1 0 0 1-2 0V6a1 1 0 0 1 2 0v5Z"/>
        </svg>
        <span class="sr-only">Warning icon</span>
    </div>`
    }

    // Close button
    const closeButton = `    <button type="button" class="ml-auto -mx-1.5 -my-1.5 bg-inigo-100 text-gray-400 hover:text-gray-900 rounded-lg focus:ring-2 focus:ring-gray-300 p-1.5 hover:bg-gray-100 inline-flex items-center justify-center h-8 w-8 dark:text-gray-500 dark:hover:text-white dark:bg-gray-800 dark:hover:bg-gray-700" data-dismiss-target="#toast-success" aria-label="Close">
        <span class="sr-only">Close</span>
        <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
        </svg>
        </button>`;

    // Append icon SVG to icon container
    iconContainer.innerHTML = iconSVG;

    // Message container
    const messageContainer = document.createElement('div');
    messageContainer.className = 'ml-3 text-sm font-normal';
    messageContainer.textContent = message;

    // Append icon container and message container to toast
    toast.appendChild(iconContainer);
    toast.appendChild(messageContainer);

    // Append close button to toast
    toast.innerHTML += closeButton;

    // Append toast to body or a specific container
    document.body.appendChild(toast);

    // Move to the top and fade out
    // Start the fade-out and move-up animation before removing the toast
    setTimeout(() => {
        toast.classList.add('toast-fade-move');
    }, 4500);
    // Remove toast after a delay
    setTimeout(() => {
        document.body.removeChild(toast);
    }, 6000);
}


// btn styling and stuff

sumHighlightBtn.addEventListener("click", function () {
    sumAttributes = true;
    sumHighlightBtn.classList.add('active');
    intHighlightBtn.classList.remove('active');
});


intHighlightBtn.addEventListener("click", function () {
    sumAttributes = false;
    intHighlightBtn.classList.add('active');
    sumHighlightBtn.classList.remove('active');

});

legBtnBoth.addEventListener("click", function () {
    leg = 'both';
    legBtnBoth.classList.add('active');
    legBtnIndividual.classList.remove('active');
    legBtnAll.classList.remove('active');

});

legBtnIndividual.addEventListener("click", function () {
    leg = 'individual';
    legBtnIndividual.classList.add('active');
    legBtnBoth.classList.remove('active');
    legBtnAll.classList.remove('active');

});

legBtnAll.addEventListener("click", function () {
    leg = 'all';
    legBtnAll.classList.add('active');
    legBtnBoth.classList.remove('active');
    legBtnIndividual.classList.remove('active');
});
