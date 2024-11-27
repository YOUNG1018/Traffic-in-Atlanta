// Function to initialize Tableau visualizations
function initializeViz(id, tableauUrl, widthPercentage) {
    var divElement = document.getElementById(id);
    var vizElement = document.createElement('object'); // Create a Tableau object
    vizElement.className = 'tableauViz'; // Add the required class
    vizElement.style.display = 'none'; // Initially hidden
    vizElement.innerHTML = `
        <param name="host_url" value="https://public.tableau.com/">
        <param name="embed_code_version" value="3">
        <param name="path" value="${tableauUrl}">
        <param name="toolbar" value="yes">
    `;
    divElement.appendChild(vizElement);

    // Function to resize visualization
    function resizeViz() {
        var pageWidth = document.documentElement.clientWidth;
        var vizWidth = pageWidth * widthPercentage;
        vizElement.style.width = vizWidth + 'px';
        vizElement.style.height = (vizWidth * 0.75) + 'px'; // Maintain aspect ratio
    }

    // Resize on window resize and initially
    resizeViz();
    window.addEventListener('resize', resizeViz);

    // Load Tableau API script
    var scriptElement = document.createElement('script');
    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
    document.body.appendChild(scriptElement);
}


// You may cumstomize the size to your vis here
document.addEventListener('DOMContentLoaded', function () {
    initializeViz('viz1732719356408', 'shared/5D8CFGWCC', 0.5); // interactive map 1 - 50%
    initializeViz('viz1732723493241', 'shared/NMMKGZX32', 0.75); // interactive map 2 -75%
    initializeViz('viz1732722871550', 'Yixuan/Map_select', 0.6); 
    initializeViz('viz1732723104838', 'Yixuan/089-3323', 0.4); 
    initializeViz('viz1732724029433', 'Yixuan/121-5468', 0.9); 
});

