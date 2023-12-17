const popupLinks = document.querySelectorAll('.catalog-item__purchase-button');
const body = document.querySelector('body');
const lockPadding = document.querySelectorAll(".lock-padding");

let unlock = true;

const timeout = 800;

if (popupLinks.length > 0) {
    for (let index = 0; index < popupLinks.length; index++) {
        const popupLink = popupLinks[index];
        popupLink.addEventListener("click", function (e) {
            const popupName = "purchase-popup";
            const currentPopup = document.getElementsByClassName(popupName);
            popupOpen(currentPopup);
            // e.preventDefault(); // ** нужно ли это?
        });
    }
}

const popupCloseIcon = document.querySelectorAll('.purchase-popup__close-button');
if (popupCloseIcon.length > 0) {
    for (let index = 0; inedx < popupCloseIcon.length; index++) {
        const closeElement = popupCloseIcon[index];
        closeElement.addEventListener('click', function(e) {
            popupCloseIcon(closeElement.closest('.purchase-popup'))
            e.preventDefault();
        })
    }
}

function popupOpen(currentPopup) {
    if (currentPopup && unlock) {
        const popupActive = document.querySelector('.purchase-popup.open');
        if (popupActive) {
            popupClose(popupActive, false);
        } else {
            bodyLock();
        }
        currentPopup.classList.add('open');
        currentPopup.addEventListener("click", function(e) {
            if (!e.target.closest('.purchase-popup__content')) {
                popupClose(e.target.closest('.purchase-popup'));
            }
        });
    }
}

function popupClose(popupActive, doUnlock = true) {
    if (unlock) {
        popupActive.classList.remove()
    }
}
