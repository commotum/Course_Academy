function toggleUnit(unitId) {
    let unitModulesDiv = $('unitModules-' + unitId);
    let unitArrow = $('unitArrow-' + unitId);


    if (unitModulesDiv.style.display === 'block') {
        unitArrow.classList.remove('unitArrowExpanded');       
        unitModulesDiv.style.display = 'none';        
    } else {
        unitArrow.classList.add('unitArrowExpanded');           
        unitModulesDiv.style.display = 'block';     
    }
}

document.body.onload = (evt) => {
    const urlParams = new URLSearchParams(window.location.search);
    const unitId = urlParams.get('unitId');

    if (unitId) {
        toggleUnit(unitId);
    }
};

