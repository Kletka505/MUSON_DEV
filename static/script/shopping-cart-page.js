const accountLogged = true;

if (accountLogged == false) {
    window.location.href = "../pages/account-page.html";
};

const itemImgValues = ["../components/main/category/items/airsoft-rifles__catalog/AGM_WWII_British_Sten_MKII.png", "../components/main/category/items/airsoft-rifles__catalog/CYMA_Standard_AK47_FullMetal.png", "../components/main/category/items/airsoft-rifles__catalog/COLT_M4A1_FullMetal_13_Keymod_Airsoft_AEG_Black.png"];
const itemNameLabelValues = ["AGM WWII British Sten MKII AEG Airsoft Rifle, Black", "CYMA Standard AK47 Full Metal Real Wood Blowback Airsoft AEG Rifle, Wood/Black", "COLT M4A1 Full Metal 13\" Keymod Airsoft AEG, Black"];
const itemPriceLabelValues = ["19990₽", "19990₽", "22490₽"];

const itemCart = document.querySelector(".item-cart")

function itemCreation(itemImgValue, itemNameLabelValue, itemPriceLabelValue) {
    let item = document.createElement('div');
    item.classList.add('item');
    item.classList.add('item_cart');
    itemCart.appendChild(item);

    let itemRow1 = document.createElement('div');
    itemRow1.classList.add('item_cart__row');
    item.appendChild(itemRow1);

    let itemRow2 = document.createElement('div');
    itemRow2.classList.add('item_cart__row');
    item.appendChild(itemRow2);

    let itemRow3 = document.createElement('div');
    itemRow3.classList.add('item_cart__row');
    item.appendChild(itemRow3);

    let itemLink1 = document.createElement('a');
    itemLink1.classList.add('item__link');
    itemLink1.classList.add('item_cart__link');
    itemLink1.href = "item-page.html";
    itemRow1.appendChild(itemLink1);
    let itemImg = document.createElement('img');
    itemImg.classList.add('item__img');
    itemImg.classList.add('item_cart__img');
    itemImg.classList.add('img-noselect');
    itemImg.src = itemImgValue;
    itemLink1.appendChild(itemImg);

    let itemLink2 = document.createElement('a');
    itemLink2.classList.add('item__link');
    itemLink2.classList.add('item_cart__link');
    itemLink2.href = "item-page.html";
    itemRow1.appendChild(itemLink2);
    let itemNameLabel = document.createElement('span');
    itemNameLabel.classList.add('item__name-label');
    itemNameLabel.classList.add('item_cart__name-label');
    itemNameLabel.textContent = itemNameLabelValue;
    itemLink2.appendChild(itemNameLabel);

    let itemPriceLabel = document.createElement('span');
    itemPriceLabel.classList.add('item__price-label');
    itemPriceLabel.classList.add('item_cart__price-label');
    itemPriceLabel.textContent = itemPriceLabelValue;
    itemRow2.appendChild(itemPriceLabel);

    let itemDeleteButton = document.createElement('button');
    itemDeleteButton.classList.add('item_cart__delete-button');
    itemDeleteButton.type = "submit";
    let itemDeleteButtonImg = document.createElement('img');
    itemDeleteButtonImg.classList.add('delete-button__img');
    itemDeleteButtonImg.src = "../components/main/category/item/item_cart__delete-button/delete-button__img.svg";
    itemDeleteButtonImg.alt = "delete-icon";
    itemDeleteButton.appendChild(itemDeleteButtonImg);
    itemRow3.appendChild(itemDeleteButton);
}

for (let i = 0; i < 3; i++) {
    itemCreation(itemImgValues[i], itemNameLabelValues[i], itemPriceLabelValues[i]);
};

const priceLabels = document.querySelectorAll(".item__price-label");
if (priceLabels.length > 0) {
    let priceSum = 0;
    for (let index = 0; index < priceLabels.length; index++) {
        // var price = toString(priceLabels[index]).slice(0, toString(priceLabels[index]).length-1);
        var price = priceLabels[index].textContent.slice(0, priceLabels[index].textContent.length-1);
        price = Number(price);
        priceSum += price;
    }
    const priceResult = document.querySelector(".result-price__number");
    priceResult.textContent = priceSum + "₽";
}

const deleteButtons = document.querySelectorAll(".item_cart__delete-button");
if (deleteButtons.length > 0) {
    for (let index = 0; index < deleteButtons.length; index++) {
        const deleteButton = deleteButtons[index];
        deleteButton.addEventListener('click', function(e) {
            deleteItem(deleteButton);
        })
    }
}

function deleteItem(deleteButton) {
    itemCart.removeChild(deleteButton.parentNode.parentNode);
}
