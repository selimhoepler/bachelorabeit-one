

//
// Data input section
//


/* TEST OBJEKT */
const test_data =
{
    "angle_moment_values": {
        "L_AnkleAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_AnkleMoment_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_ElbowAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_FootProgressAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_HeadAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_HipAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_HipMoment_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_KneeAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_KneeMoment_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_NeckAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_PelvisAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_ShoulderAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_SpineAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_ThoraxAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_WristAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_AnkleAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_AnkleMoment_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_ElbowAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_FootProgressAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_HeadAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_HipAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_HipMoment_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_KneeAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_KneeMoment_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_NeckAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_PelvisAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_ShoulderAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_SpineAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_ThoraxAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_WristAngles_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        }
    },
    "power_values": {
        "L_AnklePower_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_HipPower_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "L_KneePower_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_AnklePower_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_HipPower_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        },
        "R_KneePower_mean_norm_Verlauf": {
            "enabled": false,
            "sag": false,
            "front": false,
            "trans": false
        }
    }
}

/* TEST OBJEKT ENDE */

const dataSubmitBtn = document.getElementById('data-submit-button');
const inputFilesData = document.getElementById('input-data');
const inputFilesMetadata = document.getElementById('input-metadata');

const presetDropdown = document.getElementById("preset-dropdown");
const sendButton = document.getElementById("send-button");

const modelsButton = document.getElementById("models-button");

const executeButton = document.getElementById("execute-button");

const testButton = document.getElementById("test-button");

var checkBoxData = null;


testButton.addEventListener("click", () => {
    console.log(test_data);
    createCheckboxes(test_data);
});


dataSubmitBtn.addEventListener('click', async () => {
    // Überprüfe die Dateiendung
    const allowedExtensions = ['csv'];
    const dataFile = inputFilesData.files[0];
    const metadataFile = inputFilesMetadata.files[0];

    if (!allowedExtensions.includes(dataFile.name.split('.').pop())) {
        console.error('Fehler: Ungültige Dateierweiterung für Data-Datei');
        return;
    }

    if (!allowedExtensions.includes(metadataFile.name.split('.').pop())) {
        console.error('Fehler: Ungültige Dateierweiterung für Metadata-Datei');
        return;
    }

    // Ändere den Text auf dem Button und zeige den Ladeindikator an
    dataSubmitBtn.textContent = 'Lädt...';
    dataSubmitBtn.disabled = true;
    dataSubmitBtn.classList.remove('hover:bg-blue-600');

    // Erstelle FormData-Objekt, um Dateien zu sammeln
    const formData = new FormData();
    formData.append('data_file', dataFile, 'data.csv');
    formData.append('metadata_file', metadataFile, 'metadata.csv');

    try {
        const response = await fetch('/ingest', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            // Erfolgreich behandelt
            const data = await response.json();
            console.log(data);
            checkBoxData = data.response.checkboxes;
            console.log(checkBoxData);

            // Erstelle die Checkboxen
            createCheckboxes(checkBoxData);

            presetDropdown.disabled = false;
            sendButton.disabled = false;
            sendButton.classList.add('hover:bg-blue-600');
        } else {
            console.error('Fehler beim Senden der Dateien:', response);
        }
    } catch (error) {
        console.error('Fehler beim Senden der Dateien:', error);
    } finally {
        // Setze den Button-Text und den Ladeindikator zurück
        dataSubmitBtn.textContent = 'Submit';
        dataSubmitBtn.disabled = false;
        dataSubmitBtn.classList.add('hover:bg-blue-600');


    }
});






///
/// checkboxes Section
///



function createCheckboxes(jsonData) {
    const container = document.getElementById('checkbox-container'); // Replace with the actual container element ID

    // Parse the JSON data
    const data = jsonData;

    // Create checkboxes for angle/moment values
    for (const keys in data) {
        console.log(keys);

        for (const key in data[keys]) {
            console.log(key);

            const checkboxData = data[keys][key];
            console.log(checkboxData);
            const checkboxContainer = document.createElement('div');
            checkboxContainer.classList.add('flex');
            checkboxContainer.classList.add('justify-between');
            checkboxContainer.classList.add('checkbox-subcontainer');

            // Create enabled checkbox
            const enabledCheckbox = document.createElement('input');
            enabledCheckbox.type = 'checkbox';
            enabledCheckbox.name = key;
            enabledCheckbox.checked = checkboxData.enabled;
            // Add other attributes and event listeners as needed
            checkboxContainer.appendChild(enabledCheckbox);

            // Create label for checkbox
            const boxesLabel = document.createElement('label');
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



    // Create checkboxes for power values (similar to angle/moment values)

    // Add any additional elements or styling as needed
}

// Call the function with the received JSON data







// 
// Signal selection section
//





document.addEventListener("DOMContentLoaded", function () {


    sendButton.addEventListener("click", async () => {
        const selectedPreset = presetDropdown.value;
        /* 
        
        TESTBLOCK FOR SIGNALS JSON
        WORKS
        
        TODO: convert the presets into JS
        
        */

        const preset = getSignalJSON();



        try {
            const response = await fetch("/signals", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(preset),
            });

            if (response.ok) {
                console.log("Option erfolgreich ans Backend gesendet.");
                console.log(await response.json());
            } else {
                console.error("Fehler beim Senden der Option ans Backend:", response.statusText);
            }
        } catch (error) {
            console.error("Fehler1 beim Senden der Option ans Backend:", error);
        }



        /* 
        END OF TESTBLOCK
        
        */




        /* const question = JSON.stringify({ preset: selectedPreset });
        console.log(question);

        try {
            const response = await fetch("/signals", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: question,
            });

            if (response.ok) {
                console.log("Option erfolgreich ans Backend gesendet.");
                console.log(await response.json());
            } else {
                console.error("Fehler beim Senden der Option ans Backend:", response.statusText);
            }
        } catch (error) {
            console.error("Fehler1 beim Senden der Option ans Backend:", error);
        } */
    });
});




// function to get the signal JSON


const getSignalJSON = () => {

    const container = document.getElementById('checkbox-container');

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

            signalBoxes.forEach((signalBox, index) => {
                if (signalBox.checked) {
                    checkedColumns.push(index + index + 1);
                }
            });

            columns.push(checkedColumns);
        }
    });

    const signalData = {
        signals: signals,
        columns: columns
    }

    console.log(signalData);


    return signalData;



}


//turning presets into checkboxes

function convertPresetToCheckboxes(preset) {

    const container = document.getElementById('checkbox-container');
    const subContainer = container.querySelectorAll('.checkbox-subcontainer');
    //iterate through the subcontainers
    subContainer.forEach((subContainer) => {
        //get the checkbox
        const checkbox = subContainer.querySelector('input[type="checkbox"]');
        checkbox.checked = false
        //check if the checkbox is checked
        const checkboxName = checkbox.name;

        const matchingKey = Object.keys(preset['signals']).find(key => preset['signals'][key] === checkboxName);

        if (matchingKey) {
            // matchingKey contains the key where the value matches checkboxName
            console.log(`The checkbox name "${checkboxName}" exists in the key "${matchingKey}" in preset['signals'].`);
            checkbox.checked = true

            const signalBoxesContainer = subContainer.querySelector('.signalboxes-container');
            const signalBoxes = signalBoxesContainer.querySelectorAll('input[type="checkbox"]');



        }
    });
}



function convertPresetToCheckboxes2(preset) {
    const container = document.getElementById('checkbox-container');
    const subContainers = container.querySelectorAll('.checkbox-subcontainer');
    
    // Iterate through the subcontainers
    subContainers.forEach((subContainer, index) => {
        const checkbox = subContainer.querySelector('input[type="checkbox"]');
        const checkboxName = checkbox.name;

        // Find the index of this checkbox name in the preset signals
        const matchingIndex = preset.signals.indexOf(checkboxName);

        // If found, set the main checkbox and sub-checkboxes accordingly
        if (matchingIndex !== -1) {
            checkbox.checked = true;

            const columnIndices = preset.columns[matchingIndex];
            const signalBoxesContainer = subContainer.querySelector('.signalboxes-container');
            const signalBoxes = signalBoxesContainer.querySelectorAll('input[type="checkbox"]');

            // Reset all sub-checkboxes
            signalBoxes.forEach(box => box.checked = false);

            // Check the sub-checkboxes according to preset
            columnIndices.forEach(idx => {
                const boxIndex = (idx - 1) / 2; // Convert your 3-based index to 0-based
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






/* 
PRESETS FROM signals.JSON
-all_uc1
-thorax(andreas)
-knee_angles
-knee_angles&moments */

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

                convertPresetToCheckboxes3(myPreset);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        //uncheck all boxes
        const container = document.getElementById('checkbox-container');
        const subContainer = container.querySelectorAll('.checkbox-subcontainer');
        //iterate through the subcontainers
        subContainer.forEach((subContainer) => {
            //get the checkbox
            const checkbox = subContainer.querySelector('input[type="checkbox"]');
            checkbox.checked = false
        });
    }


}
)








//
// Model creating section
//

modelsButton.addEventListener("click", async () => {
    try {
        const response = await fetch("/models", {
            method: "GET",
        });

        if (response.ok) {
            console.log("Modelle erfolgreich ans Backend gesendet.");
            console.log(await response.json());
        } else {
            console.error("Fehler beim Senden der Modelle ans Backend:", response.statusText);
        }
    } catch (error) {
        console.error("Fehler1 beim Senden der Modelle ans Backend:", error);
    }
});


//
// Model execution section
//


function getGradientColor(value) {
    const minValue = -10; // Mindestwert der dritten Dimension
    const maxValue = 10; // Höchstwert der dritten Dimension
    const colorStart = '#0061FF'; // Anfangsfarbe (Blau)
    const colorEnd = '#C1EFFF'; // Endfarbe (Rot)

    // Berechnung des Farbwerts basierend auf dem Wert der dritten Dimension
    const ratio = (value - minValue) / (maxValue - minValue);
    const color = blendColors(colorStart, colorEnd, ratio);

    return color;
}

// Funktion zum Mischen von Farben
function blendColors(colorStart, colorEnd, ratio) {
    const r = Math.round(parseInt(colorStart.substring(1, 3), 16) * (1 - ratio) + parseInt(colorEnd.substring(1, 3), 16) * ratio);
    const g = Math.round(parseInt(colorStart.substring(3, 5), 16) * (1 - ratio) + parseInt(colorEnd.substring(3, 5), 16) * ratio);
    const b = Math.round(parseInt(colorStart.substring(5, 7), 16) * (1 - ratio) + parseInt(colorEnd.substring(5, 7), 16) * ratio);
    return `rgb(${r},${g},${b})`;
}

executeButton.addEventListener("click", async () => {
    try {
        const response = await fetch("/execute", {
            method: "GET",
        });

        if (response.ok) {
            console.log("Modelle erfolgreich executed.");

            const responseData = await response.json(); // JSON-Daten nur einmal lesen

            console.log(responseData);

            const series = responseData.scatterplot_data.map(item => ({
                x: item.x,
                y: item.y,
                // fillColor: getGradientColor(item.z)
            }));

            var options = {
                series: [{
                    name: "Sample B",
                    data: series
                }],
                chart: {
                    height: '100%',
                    type: 'scatter',
                    zoom: {
                        enabled: true,
                        type: 'xy'
                    }
                },
                xaxis: {
                    tickAmount: 10,
                    labels: {
                        formatter: function (val) {
                            return parseFloat(val).toFixed(1);
                        }
                    }
                },
                yaxis: {
                    show: false,
                    tickAmount: 7
                },
                markers: {
                    size: 8,
                    colors: series.map(item => item.fillColor)
                }
            };

            chart = new ApexCharts(document.getElementById("plot-container"), options);
            chart.render();
        } else {
            console.error("Fehler beim Senden der Modelle ans Backend:", response.statusText);
        }
    } catch (error) {
        console.error("Fehler1 beim Senden der Modelle ans Backend:", error);
    }
});








//
// Chart section
//

function tsneapex2() {

    function getGradientColor(value) {
        const minValue = -10; // Mindestwert der dritten Dimension
        const maxValue = 10; // Höchstwert der dritten Dimension
        const colorStart = '#0061FF'; // Anfangsfarbe (Blau)
        const colorEnd = '#C1EFFF'; // Endfarbe (Rot)

        // Berechnung des Farbwerts basierend auf dem Wert der dritten Dimension
        const ratio = (value - minValue) / (maxValue - minValue);
        const color = blendColors(colorStart, colorEnd, ratio);

        return color;
    }

    // Funktion zum Mischen von Farben
    function blendColors(colorStart, colorEnd, ratio) {
        const r = Math.round(parseInt(colorStart.substring(1, 3), 16) * (1 - ratio) + parseInt(colorEnd.substring(1, 3), 16) * ratio);
        const g = Math.round(parseInt(colorStart.substring(3, 5), 16) * (1 - ratio) + parseInt(colorEnd.substring(3, 5), 16) * ratio);
        const b = Math.round(parseInt(colorStart.substring(5, 7), 16) * (1 - ratio) + parseInt(colorEnd.substring(5, 7), 16) * ratio);
        return `rgb(${r},${g},${b})`;
    }




    fetch('/execute')

        .then(response => response.json())
        .then(data => {
            console.log(data)


            const series = data.scatterplot_data.map(item => ({
                x: item.x,
                y: item.y,
                // fillColor: getGradientColor(item.z)
            }));


            var options = {
                series: [
                    //         {
                    //     name: "SAMPLE A",
                    //     data: data.scatterplot_data2
                    // },
                    {
                        name: "Sample B",
                        data: series
                    }],
                chart: {
                    height: 500,
                    type: 'scatter',
                    zoom: {
                        enabled: true,
                        type: 'xy'
                    }
                },
                xaxis: {
                    tickAmount: 10,
                    labels: {
                        formatter: function (val) {
                            return parseFloat(val).toFixed(1)
                        }
                    }
                },
                yaxis: {
                    tickAmount: 7
                },

                markers: {
                    size: 8,
                    colors: series.map(item => item.fillColor)
                }
            };

            chart = new ApexCharts(document.getElementById("scatterplot"), options);
            chart.render();
        })
        .catch(error => {
            console.log('Fehler beim Abrufen der Daten:', error);
        });
}




const signalCheckboxes = () => {





}