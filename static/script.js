let currentPageIndex = 0;


const configPromise = fetch('/info')
    .then(response => response.json());


function showPage(pageIndex) {
    fetch(`/content/${pageIndex}`)
        .then(response => response.text())
        .then(text => {
                const svgContainer = document.getElementById("svgContainer");
                svgContainer.innerHTML = text;
        })
        .catch(error => console.error('Error fetching content:', error));
}


function prevPage() {
    configPromise.then(config => {
        if (currentPageIndex > 0) {
            currentPageIndex--;
            showPage(currentPageIndex);
        }
    })
}


function nextPage() {
    configPromise.then(config => {
        if (currentPageIndex < config.pageCount-1) {
            currentPageIndex++;
            showPage(currentPageIndex);
        }
    })
}


document.addEventListener('DOMContentLoaded', function () {
    showPage(0);  // Fetch and display PDF image for page 1
});

function scrollTopBy(n) {
    window.scrollBy({
        top: n,
        left: 0,
        behavior: "smooth",
    }); 
}

function scrollLeftBy(n) {
    window.scrollBy({
        top: 0,
        left: n,
        behavior: "smooth",
    }); 
}

document.addEventListener('keydown', function (event) {
    value = 50;
    if (event.ctrlKey) {
        switch (event.key) {
            case 'h':
                event.preventDefault();
                console.log('h key pressed');
                scrollLeftBy(value);
                break;
            case 'l':
                event.preventDefault();
                console.log('l key pressed');
                scrollLeftBy(-value);
                break;
            default:
                break;
        }
        return
    }
    switch (event.key) {
        case 'j':
            event.preventDefault();
            console.log('j key pressed');
            scrollTopBy(value);
            break;
        case 'k':
            event.preventDefault();
            console.log('k key pressed');
            scrollTopBy(-value);
            break;
        case 'h':
            event.preventDefault();
            console.log('h key pressed');
            prevPage();
            break;
        case 'l':
            event.preventDefault();
            console.log('l key pressed');
            nextPage();
            break;
        default:
            break;
    }
});


// Handle browser back/forward navigation
// window.onpopstate = function(event) {
//    const path = window.location.pathname;
//    const pageIndex = parseInt(path.slice(-1)) || 0;
//    
//    if (!isNaN(pageIndex)) {
//        showPage(pageIndex);
//    }
//};
