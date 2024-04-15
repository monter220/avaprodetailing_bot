globalCost = 0;
globalBonus = 0;

function serviceInputChanged() {
    changeCost();
    changeResult();
}

function bonusesChanged() {
    let bonusElem = document.getElementById('bonuses');
    let bonuses = parseInt(bonusElem.value);
    if (isNaN(bonuses)) {
        bonuses = 0;
    }
    window.globalBonus = bonuses;
    changeResult();
}

function changeResult() {
    let resultCost = document.getElementById('result-cost');
    let resultBonuses = document.getElementById('result-bonuses');

    let cost = window.globalCost;
    let bonuses = window.globalBonus;
    if (bonuses < 0) {
        cost = cost + bonuses
    }

    resultCost.textContent = cost;
    resultBonuses.textContent = bonuses;

    let serviceResultCost = document.getElementById('service-result-cost');
    let serviceResultBonus = document.getElementById('service-result-bonus');
    serviceResultCost.value = cost;
    serviceResultBonus.value = bonuses;
}

function changeCost() {
    window.globalCost = 0;
    window.globalBonus = 0;
    let services = document.querySelectorAll('.service-cost');
    services.forEach(function (elem) {
        let cost = parseInt(elem.value);
        if (isNaN(cost)) {
            cost = 0;
        }
        window.globalCost += cost;

        let bonus = Math.round(cost * parseFloat(elem.getAttribute('data-default-bonus')));
        if (isNaN(bonus)) {
            bonus = 0;
        }
        window.globalBonus += bonus;
    });
    let cost = document.getElementById('global-cost');
    cost.textContent = window.globalCost;

    let bonusElem = document.getElementById('bonuses');
    bonusElem.value = window.globalBonus;
}


function addServiceElement(id, name, cost, defaultBonus) {
    let inputContainer = document.getElementById("service-list-result");

    let div = document.createElement('div');
    div.id = "service-" + id;

    let label = document.createElement('label');
    label.setAttribute('for', 's-e' + id);
    label.textContent = name;

    let inputText = document.createElement('input');
    inputText.type = 'text';
    inputText.className = 'form-control service-cost';
    inputText.id = 's-e-' + id;
    inputText.name = 'service_cost';
    inputText.value = cost;
    inputText.required = true;
    inputText.setAttribute('data-default-bonus', defaultBonus);

    let inputHidden = document.createElement('input');
    inputHidden.type = 'hidden';
    inputHidden.className = 'form-control';
    inputHidden.name = 'service_id';
    inputHidden.value = id;
    inputHidden.required = true;

    div.appendChild(label);
    div.appendChild(inputText);
    div.appendChild(inputHidden);

    div.addEventListener("input", serviceInputChanged);

    inputContainer.appendChild(div);
}

function serviceChange(e) {
    let inputContainer = document.getElementById("service-list-result");
    let id = e.target.value;
    let name = e.target.getAttribute("data-name");
    let cost = e.target.getAttribute("data-cost");
    let defaultBonus = e.target.getAttribute("data-bonus");
    if (e.target.checked) {
        addServiceElement(id, name, cost, defaultBonus);
    } else {
        let input = document.getElementById('service-' + id);
        if (input) {
            inputContainer.removeChild(input);
        }
    }
    serviceInputChanged()
}

document.addEventListener("DOMContentLoaded", function () {
    let checkboxes = document.querySelectorAll('#service-list .form-check-input');
    checkboxes.forEach(function (elem) {
        elem.addEventListener("change", serviceChange);
    });
    let bonusElem = document.getElementById('bonuses');
    bonusElem.addEventListener("input", bonusesChanged);
});